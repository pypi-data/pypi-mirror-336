import json
from dataclasses import dataclass
from homonculi.schemas.prompt_function import PromptFunction
import re
from homonculi.text_utilities import compare_string_equality


def extract_feedback(question_data):
    for potential in (
        "correct",
        "correct_exact",
        "correct_regex",
        "wrong",
        "wrong_any",
        "feedback",
    ):
        if potential in question_data:
            return {potential: question_data.pop(potential)}
    return {}


MARKDOWN_IMAGE_URLS = re.compile(r"(?:[!]\[(?P<caption>.*?)\])\((?P<image>.*?)\)")


def extract_image_urls(markdown_text) -> list[str]:
    return [
        filename for caption, filename in MARKDOWN_IMAGE_URLS.findall(markdown_text)
    ]


@dataclass
class QuizQuestion:
    id: str
    type: str
    body: str
    points: int
    pool: str
    check: dict
    answers: list[str]
    statements: list[str]
    retainOrder: bool = False

    @staticmethod
    def from_json(question_id, data, pool):
        return QuizQuestion(
            question_id,
            data["type"],
            data["body"],
            data["points"],
            pool,
            extract_feedback(data),
            data.get("answers"),
            data.get("statements"),
            data.get("retainOrder", False),
        )

    def to_json(self):
        return {
            "type": self.type,
            "body": self.body,
            "points": self.points,
            "pool": self.pool,
            "answers": self.answers,
            "statements": self.statements,
            "retainOrder": self.retainOrder,
            **self.check,
        }

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def get_images(self):
        return extract_image_urls(self.body)


def get_id(question, index):
    return question.get("id", question.get("name", question.get("title", str(index))))


def convert_body(q):
    body = q.get("body", q.get("text", ""))
    return body


def convert_answers(q):
    answers = q.get("answers")
    if answers is None:
        return None
    if q["type"] in ("multiple_choice_question", "multiple_answers_question"):
        flattened = []
        for i, a in enumerate(answers):
            if isinstance(a, dict):
                # TODO: Incorporate the correctness
                for correctness, text in a.items():
                    flattened.append(text)
            else:
                flattened.append(a)
        return flattened
    return answers


def convert_body(q):
    body = q.get("body", q.get("text", ""))
    # Replace [[ and ]] for fill_in_multiple_blanks_question and multiple_dropdowns_question
    if q["type"] in ("fill_in_multiple_blanks_question", "multiple_dropdowns_question"):
        body = body.replace("[[", "[").replace("]]", "]")
    return body


def convert_questions(questions: list[dict]) -> list[QuizQuestion]:
    if isinstance(questions, dict):
        questions = questions.values()
    return [
        QuizQuestion(
            get_id(q, i),
            q["type"],
            convert_body(q),
            q.get("points", 1),
            q.get("pool"),
            extract_feedback(q),
            convert_answers(q),
            q.get("statements"),
            q.get("retainOrder", False),
        )
        for i, q in enumerate(questions)
        if q["type"]
        not in ("text_only_question", "essay_question", "file_upload_question")
    ]


# sys.argv[1]
def load_quiz(question_path: str) -> list[QuizQuestion]:
    with open(question_path) as f:
        quiz = json.load(f)
        pools = {q: p["name"] for p in quiz["pools"] for q in p["questions"]}
        return [
            QuizQuestion.from_json(question_id, q, pools.get(question_id))
            for question_id, q in quiz["questions"].items()
            # if q["type"] != "text_only_question"
            # and q["type"] != "fill_in_multiple_blanks_question"
        ]


def load_on_run(on_run_path: str) -> dict:
    with open(on_run_path) as f:
        return json.load(f)["questions"]


@dataclass
class ProcessedAnswer:
    original_answer: str
    answer: str
    system_error: str | None


def post_process_answer(question, answer, question_prompt_parts) -> ProcessedAnswer:
    question_type = question["type"]
    qpp_for_type = question_prompt_parts[question_type]

    use_numeric = qpp_for_type.get("use_numeric", False)

    if use_numeric:
        try:
            chosen = question["answers"][int(answer)]
            return ProcessedAnswer(answer, chosen, None)
        except:
            return ProcessedAnswer(
                answer, None, "Invalid answer index for numeric question"
            )
    else:
        return ProcessedAnswer(answer, answer, None)


def check_matching_question(student_part, correct_part) -> bool:
    if isinstance(correct_part, list):
        return student_part in correct_part
    return student_part == correct_part


def check_quiz_question(question, check, student) -> tuple[float, bool, str]:
    # TODO: Refactor this to return a dataclass instead of a tuple
    if question.get("type") == "true_false_question":
        correct = student.lower() == str(check.get("correct")).lower()
        return float(correct), correct, check.get("wrong") if not correct else "Correct"
    elif question.get("type") == "matching_question":
        corrects = [
            check_matching_question(student_part, correct_part)
            for student_part, correct_part in zip(student, check.get("correct", []))
        ]
        feedbacks = [
            feedback if isinstance(feedback, str) else feedback.get(student_part)
            for student_part, feedback in zip(student, check.get("feedback", []))
        ]
        message = (
            "\n<br>".join(map(str, feedbacks))
            if any(map(bool, feedbacks))
            else ("Correct" if all(corrects) else "Incorrect")
        )
        return sum(corrects) / len(corrects) if corrects else 0, all(corrects), message
    elif question.get("type") == "multiple_choice_question":
        if isinstance(check.get("correct"), list):
            correct = student in check.get("correct")
        else:
            correct = student == check.get("correct")
        return (
            float(correct),
            correct,
            (
                check.get("feedback", {}).get(student, "Incorrect")
                if not correct
                else "Correct"
            ),
        )
    elif question.get("type") == "multiple_answers_question":
        answers = question.get("answers", [])
        correct = {s for s in student if s in answers} == {
            s for s in check.get("correct", []) if s in answers
        }
        # correct = set(student) == set(check.get('correct', []))
        corrects = [(s in check.get("correct", [])) == (s in student) for s in answers]
        return (
            sum(corrects) / len(answers),
            correct,
            check.get("wrong_any", "Incorrect") if not correct else "Correct",
        )
    elif question.get("type") == "multiple_dropdowns_question":
        corrects = [
            student.get(blank_id) == answer
            for blank_id, answer in check.get("correct", {}).items()
        ]
        # feedbacks = "<br>\n".join(check.get('wrong', {}).get(blank_id, {}).get(answer, 'Correct')
        #             for blank_id, answer in student.items())
        feedback = (
            check.get("wrong_any", "Incorrect") if not all(corrects) else "Correct"
        )
        return sum(corrects) / len(corrects) if corrects else 0, all(corrects), feedback
    elif question.get("type") in ("short_answer_question", "numerical_question"):
        wrong_any = check.get("wrong_any", "Incorrect")
        if "correct" in check:
            correct = compare_string_equality(student, check["correct"])
            feedback = check.get("feedback", {}).get(student, wrong_any)
        elif "correct_exact" in check:
            correct = compare_string_equality(student, check["correct_exact"])
            feedback = check.get("feedback", {}).get(student, wrong_any)
        elif "correct_regex" in check:
            correct = any(re.match(reg, student) for reg in check["correct_regex"])
            feedback = [
                check.get("feedback", {}).get(reg)
                for reg in check["correct_regex"]
                if re.match(reg, student)
            ]
            feedback = feedback[0] if feedback else wrong_any
        else:
            return 0, False, "Unknown Short Answer Question Check: " + str(check)
        return float(correct), correct, feedback if not correct else "Correct"
    # TODO: Implement numerical question
    # elif question.get('type') == 'numerical_question':
    #    pass
    elif question.get("type") == "fill_in_multiple_blanks_question":
        if "correct" in check:
            corrects = [
                compare_string_equality(student.get(blank_id, ""), answer)
                for blank_id, answer in check.get("correct", {}).items()
            ]
        elif "correct_exact" in check:
            corrects = [
                compare_string_equality(student.get(blank_id, ""), answer)
                for blank_id, answer in check.get("correct_exact", {}).items()
            ]
        elif "correct_regex" in check:
            corrects = [
                any(re.match(reg, student.get(blank_id)) for reg in answer)
                for blank_id, answer in check.get("correct_regex", {}).items()
            ]
        else:
            return (
                0,
                False,
                "Unknown Fill In Multiple Blanks Question Check: " + str(check),
            )
        feedback = (
            check.get("wrong_any", "Incorrect") if not all(corrects) else "Correct"
        )
        return sum(corrects) / len(corrects) if corrects else 0, all(corrects), feedback
    elif question.get("type") in ("text_only_question", "essay_question"):
        return 1, True, "Correct"
    return None
