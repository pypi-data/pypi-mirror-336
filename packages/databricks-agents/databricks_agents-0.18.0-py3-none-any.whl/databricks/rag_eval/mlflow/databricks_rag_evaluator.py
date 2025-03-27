import json
import logging
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import mlflow
import mlflow.entities as mlflow_entities
import mlflow.tracing.constant as tracing_constant
import pandas as pd
from jinja2 import Environment, PackageLoader, select_autoescape
from mlflow import models as mlflow_models
from mlflow.models import evaluation as mlflow_evaluation
from mlflow.models.evaluation import artifacts as mlflow_artifacts
from mlflow.utils import mlflow_tags

from databricks.rag_eval import (
    constants,
    context,
    env_vars,
    evaluator_plugin,
    schemas,
    session,
)
from databricks.rag_eval.config import evaluation_config
from databricks.rag_eval.evaluation import entities, harness, per_run_metrics
from databricks.rag_eval.mlflow import eval_logging, mlflow_utils
from databricks.rag_eval.utils import error_utils, workspace_url_resolver

_logger = logging.getLogger(__name__)


def _log_pandas_df_artifact(pandas_df, artifact_name):
    """
    Logs a pandas DataFrame as a JSON artifact, then returns an EvaluationArtifact object.
    """
    mlflow_artifact_name = f"{artifact_name}.json"
    mlflow.log_table(pandas_df, mlflow_artifact_name)
    return mlflow_artifacts.JsonEvaluationArtifact(
        uri=mlflow.get_artifact_uri(mlflow_artifact_name),
    )


def _count_passing(results_df: pd.DataFrame) -> Optional[int]:
    """
    Counts the number of rows that are considered passing in the evaluation results.

    For now, we consider a row passing if the overall assessment rating is YES.

    Return None if the overall assessment column is not present in the results_df.

    :param results_df: DataFrame containing evaluation results
    :return: Number of rows that are considered passing
    """
    overall_assessment_rating_col = schemas.OVERALL_ASSESSMENT_RATING_COL
    return (
        (
            results_df[overall_assessment_rating_col] == entities.CategoricalRating.YES
        ).sum()
        if overall_assessment_rating_col in results_df.columns
        else None
    )


def generate_summary(results_df: pd.DataFrame) -> Optional[str]:
    """
    Generates a short summary of the evaluation results suitable for printing.

    :param results_df: DataFrame containing evaluation results
    :return: A summary string.
    """

    num_rows = len(results_df)
    num_passing = _count_passing(results_df)

    return f"{num_passing}/{num_rows} pass" if num_passing is not None else None


# Used to display summary and instructions to the user after evaluation is complete.
_AI_ICON_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 16 16" aria-hidden="true" focusable="false" class=""><path fill="currentColor" fill-rule="evenodd" d="M10.726 8.813 13.199 8l-2.473-.813a3 3 0 0 1-1.913-1.913L8 2.801l-.813 2.473a3 3 0 0 1-1.913 1.913L2.801 8l2.473.813a3 3 0 0 1 1.913 1.913L8 13.199l.813-2.473a3 3 0 0 1 1.913-1.913Zm2.941.612c1.376-.452 1.376-2.398 0-2.85l-2.473-.813a1.5 1.5 0 0 1-.956-.956l-.813-2.473c-.452-1.376-2.398-1.376-2.85 0l-.813 2.473a1.5 1.5 0 0 1-.956.956l-2.473.813c-1.376.452-1.376 2.398 0 2.85l2.473.813a1.5 1.5 0 0 1 .956.957l.813 2.472c.452 1.376 2.398 1.376 2.85 0l.813-2.473a1.5 1.5 0 0 1 .957-.956l2.472-.813Z" clip-rule="evenodd"></path></svg>
"""


def _display_summary_and_usage_instructions(run_id: str, results_df: pd.DataFrame):
    """
    Displays summary of the evaluation result, errors and warnings if any,
    and instructions on what to do after running `mlflow.evaluate`.
    """

    summary_text = generate_summary(results_df)

    run = mlflow.get_run(run_id)
    if mlflow_tags.MLFLOW_DATABRICKS_WORKSPACE_URL in run.data.tags:
        # Include Databricks URLs in the displayed message.
        workspace_url = run.data.tags[mlflow_tags.MLFLOW_DATABRICKS_WORKSPACE_URL]
        resolver = workspace_url_resolver.WorkspaceUrlResolver(workspace_url)
        eval_results_url = resolver.resolve_url_for_mlflow_evaluation_results(run.info)

        # Create a Jinja2 environment and load the template
        env = Environment(
            loader=PackageLoader("databricks.rag_eval", "templates"),
            autoescape=select_autoescape(["html"]),
        )
        template = env.get_template("eval_output.html")

        # Render the template with the data
        rendered_html = template.render(
            {
                "summary_text": summary_text,
                "eval_results_url": eval_results_url,
            }
        )

        context.get_context().display_html(rendered_html)
    else:
        print(
            f"""Evaluation completed{": " + summary_text if summary_text else "."}

Metrics and evaluation results can be viewed from the MLflow run page.
To compare evaluation results across runs, view the "Evaluation" tab of the experiment.

Get aggregate metrics: `result.metrics`.
Get per-row evaluation results: `result.tables['eval_results']`.
`result` is the `EvaluationResult` object returned by `mlflow.evaluate`.
"""
        )


def _log_evaluation_input_artifacts(
    config: evaluation_config.EvaluationConfig, examples_df: Optional[pd.DataFrame]
):
    """
    Logs the configuration to MLflow, as well as the examples_df if provided.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir, "eval_config.json")
        config_str = json.dumps(config.to_dict())
        path.write_text(config_str)
        mlflow.log_artifact(str(path))

    if examples_df is not None:
        _log_pandas_df_artifact(examples_df, "eval_examples")


_FAIL_TO_GET_TRACE_WARNING_MSG = re.compile(
    r"Failed to get trace from the tracking store"
)


def _log_traces_and_assessments(
    experiment_id: str,
    run_id: Optional[str],
    eval_results: list[entities.EvalResult],
):
    """
    Log all traces and assessments to MLflow.

    A trace acts as a storage container for all of our judge assessments and metrics. Thus, we
    ensure that MLFlow has a trace for every eval row.

    A trace may have been generated and logged during model invocation, in which case we don't
    need to create a trace. However, if a trace was passed in as part of the eval row, we need to
    make a copy, because we don't know if the trace was used in a previous eval invocation. Without
    a copy, we could end up with multiple evaluation runs adding assessments to the same trace.

    The trace objects will be mutated to extend their trace.info.assessments with the newly
    logged assessments.
    """
    with mlflow.utils.logging_utils.suppress_logs(
        mlflow.tracing.fluent.__name__, _FAIL_TO_GET_TRACE_WARNING_MSG
    ):
        for eval_result in eval_results:
            trace = eval_result.eval_item.trace

            # Ensure that every trace is logged in MLflow, regardless of where it came from.
            # Specifically, if the trace is present in MLflow, do nothing. Otherwise, log the trace.
            if (
                trace.info.request_id is None
                or mlflow.get_trace(trace.info.request_id) is None
            ):
                trace.info.experiment_id = experiment_id
                if run_id is not None:
                    trace.info.request_metadata[
                        tracing_constant.TraceMetadataKey.SOURCE_RUN
                    ] = run_id

                mlflow_client = mlflow.MlflowClient()
                try:
                    # TODO(ML-51635): Add retries to failures
                    stored_trace_id = mlflow_client._log_trace(trace)
                    # TODO(ML-51100): Migrate to using mlflow.log_trace() when this API is available.
                    # log_trace uses traceV3, and accepts client-generated trace_id.
                    # This makes trace.info.trace_id consistent with trace.data.span[].context.trace_id
                    # and the trace_ids on the assessments.
                    trace.info.request_id = stored_trace_id
                except Exception as e:
                    _logger.warning(f"Failed to log the trace: {e}")
                    continue

            if env_vars.AGENT_EVAL_LOG_TO_MLFLOW_ENABLED.get():
                # Create the assessments
                assessments = eval_result.assessments
                for assessment in assessments:
                    # Ensure that if we created a new trace, that the updated trace_id is reflected in
                    # the assessments.
                    assessment.trace_id = trace.info.request_id
                    assessment.metadata = (
                        {**assessment.metadata, "run_id": run_id}
                        if assessment.metadata is not None
                        else {"run_id": run_id}
                    )
                    _log_assessment_to_mlflow(assessment)

            # At this point, eval_result.assessments is a stale field, because when we create
            # the assessments, they have their assessment_ids assigned.
            # However, eval_result.assessments is never end-user visible, so this is fine.

            # Refresh the trace to fetch newly created assessments, complete with assessment_ids.
            eval_result.trace = mlflow.get_trace(trace.info.request_id)


def _log_assessment_to_mlflow(
    assessment: mlflow_entities.Assessment,
) -> mlflow_entities.Assessment:
    """
    Creates the given assessment in MLflow.
    """
    # Note that the `log_expectation` and `log_feedback` APIs expect the ID without the "0x" prefix.
    # However, the `encode_trace_id` utility adds the "0x" prefix so we add this check.
    span_id = assessment.span_id.removeprefix("0x")
    # TODO(ML-51635): Add retries to failures
    if assessment.expectation is not None:
        return mlflow.log_expectation(
            trace_id=assessment.trace_id,
            name=assessment.name,
            source=assessment.source,
            value=assessment.expectation.value,
            metadata=assessment.metadata,
            span_id=span_id,
        )
    else:
        if assessment.error is not None:
            error = assessment.error
            value = None
        else:
            error = None
            value = assessment.feedback.value

        return mlflow.log_feedback(
            trace_id=assessment.trace_id,
            name=assessment.name,
            source=assessment.source,
            error=error,
            value=value,
            rationale=assessment.rationale,
            metadata=assessment.metadata,
            span_id=span_id,
        )


class DatabricksRagEvaluator(mlflow_evaluation.base.ModelEvaluator):
    @classmethod
    def can_evaluate(cls, *, model_type, evaluator_config, **kwargs) -> bool:
        """
        See parent class docstring.
        """
        return model_type == evaluator_plugin.MODEL_TYPE

    @context.eval_context
    def evaluate(
        self,
        *,
        model_type,
        dataset,
        run_id,
        evaluator_config: Optional[Dict[str, Any]] = None,
        model=None,
        custom_metrics=None,
        extra_metrics=None,
        custom_artifacts=None,
        baseline_model=None,
        predictions=None,
        **kwargs,
    ):
        """
        Runs Databricks RAG evaluation on the provided dataset.

        The following arguments are supported:
        - model_type: Must be the same as evaluator_plugin.MODEL_TYPE
        - dataset
        - run_id

        For more details, see parent class docstring.
        """
        try:
            if evaluator_config is None:
                evaluator_config = {}

            config = evaluation_config.EvaluationConfig.from_mlflow_evaluate_args(
                evaluator_config, extra_metrics
            )

            eval_dataset = mlflow_utils.mlflow_dataset_to_evaluation_dataset(dataset)

            # Set batch size to the context
            session.current_session().set_session_batch_size(
                len(eval_dataset.eval_items)
            )
            run_info = mlflow.get_run(run_id)
            experiment_id = run_info.info.experiment_id

            eval_results = harness.run(
                model=model,
                eval_dataset=eval_dataset,
                config=config,
                experiment_id=experiment_id,
                run_id=run_id,
            )
            # TODO(ML-51636): Move this into `harness.run` to parallelize
            _log_traces_and_assessments(experiment_id, run_id, eval_results)

            mlflow_per_run_metrics = per_run_metrics.generate_per_run_metrics(
                eval_results
            )

            # Log results to mlflow
            examples_df: pd.DataFrame = evaluator_config.get(
                constants.EVALUATOR_CONFIG_EXAMPLES_KEY_NAME, None
            )

            _log_evaluation_input_artifacts(config, examples_df)

            mlflow.log_metrics(mlflow_per_run_metrics)

            eval_results_df = pd.DataFrame(
                [result.to_pd_series() for result in eval_results]
            )

            eval_results_artifact = _log_pandas_df_artifact(
                eval_results_df, "eval_results"
            )

            eval_logging.log_eval_results(eval_results)

            _display_summary_and_usage_instructions(run_id, eval_results_df)

            result = mlflow_models.EvaluationResult(
                metrics=mlflow_per_run_metrics,
                artifacts={"eval_results": eval_results_artifact},
            )

            return result
        except error_utils.ValidationError as e:
            # Scrub trace for user-facing validation errors
            raise error_utils.ValidationError(str(e)) from None
