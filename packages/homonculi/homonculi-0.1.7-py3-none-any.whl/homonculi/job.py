import time
from collections import defaultdict
from dataclasses import dataclass, field
from homonculi.config import Configuration
from homonculi.quizzes.loader import QuizFile
from homonculi.schemas.prompt_function import PromptCollection


@dataclass
class ResultRow:
    question_id: str
    student_id: str
    attempt: int
    answer: str
    confidence: str
    score: float
    correct: bool
    points: float
    weighted: float
    system_error: str
    feedback: str
    mistake: str
    reason: str

    def to_csv(self, with_confidence: bool = True) -> list:
        return (
            [self.question_id, self.student_id, self.attempt, self.answer]
            + ([self.confidence] if with_confidence else [])
            + [
                self.score,
                self.correct,
                self.points,
                self.weighted,
                self.system_error,
                self.feedback,
                self.mistake,
                self.reason,
            ]
        )


RESULT_HEADERS = [
    "QuestionID",
    "StudentID",
    "Attempt",
    "Answer",
    "Confidence",
    "Score",
    "Correct",
    "PointsPossible",
    "Weighted",
    "SystemError",
    "Feedback",
    "Mistake",
    "Reason",
]
WITHOUT_CONFIDENCE = [header for header in RESULT_HEADERS if header != "Confidence"]


@dataclass
class JobData:
    config: Configuration
    quiz: QuizFile
    prompts: PromptCollection
    runs: list = field(default_factory=list)
    time_started: int = field(default_factory=lambda: int(time.time()))
    time_finished: int | None = None
    created_prompts: dict[str, dict[str, str]] = field(
        default_factory=lambda: defaultdict(dict)
    )

    def to_json(self) -> str:
        return {
            "config": self.config.to_json(),
            "quiz": self.quiz.to_json(),
            "prompts": self.prompts.to_json(),
            "runs": self.runs,
            "time_started": self.time_started,
            "time_finished": self.time_finished,
        }
