import dataclasses
from typing import Literal, Protocol


class AssessmentConfig(Protocol): ...


AI_JUDGE_SAFETY = "safety"
AI_JUDGE_GROUNDEDNESS = "groundedness"
AI_JUDGE_RELEVANCE_TO_QUERY = "relevance_to_query"
AI_JUDGE_CHUNK_RELEVANCE = "chunk_relevance"
AI_JUDGE_GUIDELINE_ADHERENCE = "guideline_adherence"


_BUILT_IN_JUDGE_NAMES = [
    AI_JUDGE_SAFETY,
    AI_JUDGE_GROUNDEDNESS,
    AI_JUDGE_RELEVANCE_TO_QUERY,
    AI_JUDGE_CHUNK_RELEVANCE,
]


@dataclasses.dataclass
class BuiltinJudge(AssessmentConfig):
    """Configuration for a builtin judge to be run on traces from a GenAI application.

    Raises:
        ValueError: When the judge name is invalid.
    """

    name: Literal["safety", "groundedness", "relevance_to_query", "chunk_relevance"]

    def __post_init__(self):
        if isinstance(self.name, str):
            if self.name not in _BUILT_IN_JUDGE_NAMES:
                raise ValueError(
                    f"Invalid judge name '{self.name}'. Must be oneof {_BUILT_IN_JUDGE_NAMES}."
                )
            return


@dataclasses.dataclass
class GuidelinesJudge(AssessmentConfig):
    """Configuration for a guideline adherence judge to be run on traces from an GenAI application.

    Raises:
        ValueError: When there are duplicate keys in `guidelines` dict.
        ValueError: When there are duplicate values for a key in `guidelines` dict.
    """

    guidelines: dict[str, list[str]]

    def __post_init__(self):
        if self.guidelines is None:
            raise ValueError("guidelines cannot be None")

        # This warning message is necessary as the server can set an
        # empty guidelines judge as a default.
        if len(self.guidelines) == 0:
            print("WARNING: Your guidelines adherence judge has no guidelines.")
            return

        for key, values in self.guidelines.items():
            # check for empty guideline values within each key
            if not values:
                raise ValueError(
                    f"Empty values found for key '{key}' in `guidelines` dict."
                )

            # check for duplicate guideline values within each key
            if len(values) != len(set(values)):

                raise ValueError(
                    f"Duplicate values found for key '{key}' in `guidelines` dict."
                )


@dataclasses.dataclass
class AssessmentsSuiteConfig:
    """Configuration for a suite of assessments to be run on traces from a GenAI application.

    Raises:
        ValueError: When sample is not between 0.0 (exclusive) and 1.0 (inclusive).
        ValueError: When more than one guidelines judge is found.
        ValueError: When duplicate builtin judges are found.
    """

    sample: float | None = None
    paused: bool | None = None
    assessments: list[AssessmentConfig] | None = None

    def __post_init__(self):
        if self.sample is not None and not (0.0 < self.sample <= 1.0):
            raise ValueError(
                "Sample must be between 0.0 (exclusive) and 1.0 (inclusive)."
            )

        if self.assessments is None:
            return

        # Enforce unique metrics
        seen_preset_judges = set()
        for assessment in self.assessments:
            if isinstance(assessment, BuiltinJudge):
                if str(assessment.name) in seen_preset_judges:
                    raise ValueError(
                        f'Duplicate builtin judge found: "{assessment.name}"'
                    )
                seen_preset_judges.add(str(assessment.name))

        # Enforce one guidelines judge in assessments
        if (
            len(
                list(filter(lambda a: isinstance(a, GuidelinesJudge), self.assessments))
            )
            > 1
        ):
            raise ValueError("Only one guidelines judge is allowed in assessments.")

    @classmethod
    def from_dict(cls, data: dict):
        assessments: list[AssessmentConfig] | None = None
        if "assessments" in data:
            assessments = []
            for assessment in data["assessments"]:
                if assessment["name"] == AI_JUDGE_GUIDELINE_ADHERENCE:
                    assessments.append(
                        GuidelinesJudge(
                            guidelines=assessment["guidelines"],
                        )
                    )
                    continue
                assessments.append(BuiltinJudge(name=assessment["name"]))

        return cls(
            sample=data.get("sample"),
            paused=data.get("paused"),
            assessments=assessments,
        )
