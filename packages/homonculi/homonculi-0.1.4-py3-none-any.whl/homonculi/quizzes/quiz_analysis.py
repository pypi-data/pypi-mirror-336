"""
Process canvas quizzes to make them easier to parse
"""

from collections import defaultdict
from textwrap import indent
from pprint import pprint

from markdown import Markdown
from dataclasses import dataclass
import re

from html.parser import HTMLParser
from math import isnan

from homonculi.stats_utilities import correlation, binconf
from homonculi.quizzes.quizzes import process_quiz_str, try_parse_file
from homonculi.text_utilities import compare_string_equality


def check_entered_string(value, check, key):
    if "correct" in check:
        return compare_string_equality(value, check.get("correct", {}).get(key, []))
    elif "correct_exact" in check:
        return compare_string_equality(
            value, check.get("correct_exact", {}).get(key, [])
        )
    elif "correct_regex" in check:
        return any(
            re.match(str(reg), value)
            for reg in check.get("correct_regex", {}).get(key, "")
        )


def make_readonly_quiz_body(question, feedback, student, check, is_grader):
    text = question["body"]
    if question["type"] in (
        "multiple_dropdowns_question",
        "fill_in_multiple_blanks_question",
    ):
        for key, value in student.items():
            correct = check_entered_string(value, check, key)
            text = re.sub(
                rf"(?<!\\)(\[{key}\])(?!\()",
                f"<span class='mdq mdq-{correct if is_grader else 'unknown'}'>{value}</span>",
                text,
            )
    return Markdown(extensions=["fenced_code"]).convert(text)


def check_matching_question(student, check):
    if isinstance(check, str):
        return student == check
    return student in check


def check_quiz_answer(question, feedback, student, check, is_grader, part=None):
    if question["type"] == "true_false_question":
        return (
            student.lower() == str(check.get("correct")).lower()
            if is_grader
            else "unknown"
        )
    elif question["type"] == "multiple_answers_question":
        return (part in check.get("correct", [])) == (part in student)
    elif question["type"] == "matching_question":
        return check_matching_question(student, check.get("correct", [])[part])
    elif question["type"] == "multiple_choice_question":
        if isinstance(check.get("correct"), list):
            return student in check.get("correct")
        return student == check.get("correct")
    elif question["type"] in ("short_answer_question", "numerical_question"):
        if "correct_exact" in check:
            return compare_string_equality(student, check["correct_exact"])
        elif "correct_regex" in check:
            return any(re.match(reg, student) for reg in check["correct_regex"])
        else:
            return False
    elif question["type"] in (
        "multiple_dropdowns_question",
        "fill_in_multiple_blanks_question",
    ):
        return check_entered_string(student, check, part)


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def to_percent(a_value):
    if isnan(a_value):
        return "NaN%"
    return str(int(round(a_value * 1000)) / 10) + "%"


def clean_text(text):
    return text.replace("\\", "")


def to_python_name(s):
    # Remove invalid characters
    s = re.sub("[^0-9a-zA-Z_]", "", s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub("^[^a-zA-Z_]+", "", s)
    return s


def fill_nan_str(value):
    if isinstance(value, float) and isnan(value):
        return ""
    else:
        return str(value)


def split_on_commas(text):
    return re.split(r"(?<!\\),", text)


def sort_by_value_count(pair):
    value, (count, multiples, initials) = pair
    return value, -count


def sort_by_count(pair):
    value, (count, multiples, initials) = pair
    return -count


"""
% of students who chose it at some point
% of students who chose it on their initial submission
% of students who chose it on their final submission
"""


class QuizQuestionType:
    name = "Abstract Quiz Question Type"

    @staticmethod
    def key_occurrences(value):
        return sort_by_value_count(value)

    def __init__(
        self,
        question,
        submissions,
        attempts,
        user_ids,
        submission_scores,
        quiz_scores,
        course_scores,
        max_score,
        anonymous,
        path,
        quiz,
        position,
    ):
        # Critical Information
        self.quiz = quiz
        self.question = question
        self.submissions = submissions
        self.attempts = attempts
        self.position = position
        if user_ids is None:
            user_ids = ["Anon " + str(i) for i in range(len(submissions))]
        self.user_ids = user_ids
        self.uas = zip(user_ids, attempts, submissions)
        self.scores = list(zip(user_ids, attempts, submission_scores, quiz_scores))
        self.course_scores = course_scores
        self.max_score = max_score
        self.anonymous = anonymous
        self.path = path
        # Decorative information
        self.question_name = question["question_name"]
        self.points_possible = question["points_possible"]
        self.text = question["question_text"]
        # Helper information
        self.total_submissions = len(submissions)
        self.total_students = len(set(user_ids))
        self.final_submission = {
            user_id: attempt for attempt, user_id in sorted(zip(attempts, user_ids))
        }
        # Calculated Information
        self.results = []

        self.prepare_corrects()

    def analyze(self):
        pass

    def to_answers(self):
        yield from self.break_up_submission()

    def to_json(self):
        quiz_disc, course_disc = self.calculate_discrimination()
        o_diff, i_diff, f_diff = self.calculate_difficulty()
        return {
            "question_name": self.question_name,
            "name": self.name,
            "path": self.path,
            "anonymous": self.anonymous,
            "points_possible": self.points_possible,
            "text": self.text,
            "discrimination": {"quiz": quiz_disc, "course": course_disc},
            "difficulty": {"overall": o_diff, "initial": i_diff, "final": f_diff},
        }

    def to_text(self):
        body = [
            self.question_name,
            "\t" + self.name,
            "\t" + str(self.points_possible) + " points",
            indent(strip_tags(self.text.strip()), "\t"),
            "\t---Discrimination---",
        ]
        quiz, course = self.calculate_discrimination()
        body.append("\tQuiz: {}".format(to_percent(quiz)))
        body.append("\tCourse: {}".format(to_percent(course)))
        o_diff, i_diff, f_diff = self.calculate_difficulty()
        if o_diff is not None:
            body.append("\t---Difficulty---")
            body.append("\tOverall: {}".format(to_percent(o_diff)))
            body.append("\tInitial: {}".format(to_percent(i_diff)))
            body.append("\tFinal: {}".format(to_percent(f_diff)))
        body.append("\t---Answers---")
        body.extend(self.to_text_answers())
        return "\n".join(body)

    def to_text_answers(self):
        body = []
        for answer, correct, o, i, f in self.results:
            body.append(
                ""
                + "\t{},\t{},\t{}:{}\t".format(
                    *map(to_percent, (o, i, f)), ("*" if correct else "")
                )
                + strip_tags(answer)
            )
        return body

    def score_occurrences(self, occurrences, correctness):
        self.results = []
        sorted_occurrences = sorted(occurrences.items(), key=self.key_occurrences)
        self.quiz_discrimination = []
        self.course_discrimiation = []
        for key, (count, initials, finals) in sorted_occurrences:
            is_correct = correctness(key)
            o_score = count / self.total_submissions
            i_score = len(initials) / self.total_students
            f_score = len(finals) / self.total_students
            self.results.append((key, is_correct, o_score, i_score, f_score))

    def check_answers(self, submission):
        return [(self.question_name, clean_text(submission), "Unknown")]

    def prepare_corrects(self):
        pass

    def submission_keys(self, submission):
        """
        Find all the possible subquestions and parts to this
        submission, generate keys in the occurrence dictionary
        for them.
        """
        return (clean_text(submission),)

    def count_occurrences(self):
        occurrences = defaultdict(lambda: [0, set(), set()])
        for user_id, attempt, submission in self.uas:
            submission = fill_nan_str(submission)
            for key in self.submission_keys(submission):
                count, initials, finals = occurrences[key]
                occurrences[key][0] += 1
                if attempt == 1:
                    initials.add(user_id)
                if self.final_submission[user_id] == attempt:
                    finals.add(user_id)
        return occurrences

    def break_up_submission(self):
        for user_id, attempt, submission in self.uas:
            submission = fill_nan_str(submission)
            for subquestion, subanswer, correct in self.check_answers(submission):
                # unique_keys = self.submission_keys(submission)
                # print(unique_key)
                # for unique_key in unique_keys:
                yield [
                    type(self).__name__,
                    user_id,
                    self.quiz["title"],
                    self.question_name,
                    self.question["question_text"],
                    attempt,
                    subquestion,
                    subanswer,
                    correct,
                ]

    def calculate_discrimination(self):
        initial_quizzes = []
        initial_courses = []
        for user_id, attempt, submission, quiz in self.scores:
            if attempt == 1:
                initial_quizzes.append((submission, quiz))
                if user_id in self.course_scores:
                    course = self.course_scores[user_id]
                    initial_courses.append((submission, course))
        quiz, _ = correlation(*zip(*initial_quizzes))
        if initial_courses:
            course, _ = correlation(*zip(*initial_courses))
        else:
            course = float("nan")
        return quiz, course

    def calculate_difficulty(self):
        if not self.max_score:
            return 0, 0, 0
        total = 0
        initial = 0
        final = 0
        for user_id, attempt, submission, quiz in self.scores:
            total += submission
            if attempt == 1:
                initial += submission
            elif self.final_submission[user_id] == attempt:
                final += submission
        o_score = total / (self.total_submissions * self.max_score)
        i_score = initial / (self.total_students * self.max_score)
        f_score = final / (self.total_students * self.max_score)
        return o_score, i_score, f_score


class ShortAnswerQuestion(QuizQuestionType):
    name = "Short Answer Question"

    @staticmethod
    def key_occurrences(value):
        return sort_by_count(value)

    def single_correctness(self, value):
        return value in (
            answer["text"] if answer["text"] else strip_tags(answer["html"])
            for answer in self.question["answers"]
        )

    def analyze(self):
        occurrences = self.count_occurrences()
        self.score_occurrences(occurrences, self.single_correctness)

    def check_answers(self, submission):
        return [
            (
                self.question_name,
                clean_text(submission),
                self.single_correctness(submission),
            )
        ]

    def to_question(self):
        pass


class MatchingQuestions(QuizQuestionType):
    name = "Matching Question"

    def prepare_corrects(self):
        self.correct_answers = {
            answer["left"]: answer["right"] for answer in self.question["answers"]
        }

    def single_correctness(self, value):
        left, right = value
        # TODO: Fix this hack, why does it work?
        # Specific case was "True"
        if left not in self.correct_answers:
            left = '"{}"'.format(left)
        return right == self.correct_answers.get(left, None)

    def analyze(self):
        occurrences = self.count_occurrences()
        self.score_occurrences(occurrences, self.single_correctness)

    def check_answers(self, submission):
        for answer in split_on_commas(submission):
            if not answer:
                continue
            key, value = map(clean_text, answer.split("=>"))
            yield (key, value, self.single_correctness((key, value)))

    def submission_keys(self, submission):
        for answer in split_on_commas(submission):
            if not answer:
                continue
            key, value = map(clean_text, answer.split("=>"))
            yield (key, value)

    def to_text_answers(self):
        body = []
        previous_label = None
        for (key, value), correct, o, i, f in self.results:
            if previous_label != key:
                body.append("\t" + key)
            body.append(
                "\t\t{},\t{},\t{}:{}\t".format(
                    *map(to_percent, (o, i, f)), ("*" if correct else "")
                )
                + strip_tags(value)
            )
            previous_label = key
        return body


class FillInMultipleBlanks(QuizQuestionType):
    name = "Fill in Multiple Blanks"

    def submission_keys(self, submission):
        for label, answer in zip(self.labels, split_on_commas(submission)):
            label = clean_text(label)
            answer = clean_text(answer)
            yield (label, answer)

    def prepare_corrects(self):
        # Retrieve all possible answers
        possible_answers = defaultdict(list)
        self.labels = []
        for answer in self.question["answers"]:
            blank_id = answer["blank_id"]
            cleaned_text = clean_text(answer["text"])
            possible_answers[blank_id].append(cleaned_text)
            if blank_id not in self.labels:
                self.labels.append(blank_id)
        self.possible_answers = possible_answers

    def single_correctness(self, value):
        # Calculate correctness
        label, given = value
        return given in self.possible_answers[label]

    def check_answers(self, submission):
        for label, answer in zip(self.labels, split_on_commas(submission)):
            label = clean_text(label)
            answer = clean_text(answer)
            yield (label, answer, self.single_correctness((label, answer)))

    def analyze(self):
        # Calculate occurrences of each possible answer
        occurrences = self.count_occurrences()
        self.score_occurrences(occurrences, self.single_correctness)

    def to_text_answers(self):
        body = []
        previous_label = None
        for (label, answer), correct, o, i, f in self.results:
            if previous_label != label:
                body.append("\t" + label)
            body.append(
                "\t\t{},\t{},\t{}:{}\t".format(
                    *map(to_percent, (o, i, f)), ("*" if correct else "")
                )
                + strip_tags(answer)
            )
            previous_label = label
        return body


class MultipleChoiceQuestion(QuizQuestionType):
    name = "Multiple Choice Question"

    def prepare_corrects(self):
        self.answers = [
            str(answer["text"]) if answer["text"] else strip_tags(answer["html"])
            for answer in self.question["answers"]
            if answer["weight"]
        ]

    def single_correctness(self, value):
        # TODO: Fix this hack, why does it work?
        # Specific case was "True"
        if value not in self.answers:
            value = '"{}"'.format(value)
        return value in self.answers

    def check_answers(self, submission):
        return [
            (
                self.question_name,
                clean_text(submission),
                self.single_correctness(submission),
            )
        ]

    def analyze(self):
        occurrences = self.count_occurrences()
        self.score_occurrences(occurrences, self.single_correctness)


class MultipleAnswersQuestion(QuizQuestionType):
    name = "Multiple Answers Question"

    def submission_keys(self, submission):
        for answer in split_on_commas(submission):
            yield clean_text(answer)

    def check_answers(self, submission):
        given_answers = [clean_text(s) for s in split_on_commas(submission)]
        for label in self.labels:
            student_answered = label in given_answers
            yield (
                label,
                student_answered,
                (label in self.possible_answers) == student_answered,
            )

    def prepare_corrects(self):
        # self.answers = [str(answer['text']) if answer['text']
        #           else strip_tags(answer['html'])
        #           for answer in self.question['answers']
        #           if answer['weight']]

        self.possible_answers = []
        self.labels = []
        for answer in self.question["answers"]:
            cleaned_text = (
                str(answer["text"]) if answer["text"] else strip_tags(answer["html"])
            )
            self.labels.append(cleaned_text)
            if answer["weight"]:
                self.possible_answers.append(cleaned_text)

    def single_correctness(self, value):
        return value in self.possible_answers

    def analyze(self):
        occurrences = self.count_occurrences()
        self.score_occurrences(occurrences, self.single_correctness)


class MultipleDropDownsQuestion(FillInMultipleBlanks):
    name = "Multiple Drop-Down Question"


class TrueFalseQuestion(MultipleChoiceQuestion):
    name = "True/False Questions"


class EssayQuestion(QuizQuestionType):
    name = "Essay Quesion"

    def check_answers(self, submission):
        return [(self.question_name, clean_text(submission), "Unknown")]

    def analyze(self):
        self.results = list(self.submissions)

    def to_text(self):
        return self.name


class TextOnlyQuestion(QuizQuestionType):
    def analyze(self):
        self.results = []

    def to_text(self):
        return self.name

    def check_answers(self, submission):
        return [(self.question_name, clean_text(submission), "Unknown")]


class DefaultQuestionType(QuizQuestionType):
    def calculate_difficulty(self):
        return 0, 0, 0

    def calculate_discrimination(self):
        return 0, 0

    def analyze(self):
        self.results = []

    def to_text(self):
        return self.name


QUESTION_TYPES = {
    "fill_in_multiple_blanks_question": FillInMultipleBlanks,
    "matching_question": MatchingQuestions,
    "short_answer_question": ShortAnswerQuestion,
    "multiple_choice_question": MultipleChoiceQuestion,
    "multiple_answers_question": MultipleAnswersQuestion,
    "true_false_question": TrueFalseQuestion,
    "multiple_dropdowns_question": MultipleDropDownsQuestion,
    "essay_question": EssayQuestion,
    "text_only_question": TextOnlyQuestion,
}


@dataclass
class QuizQuestionAttempt:
    correct: bool
    score: float
    overall_score: float


@dataclass
class QuizQuestionPart:
    key: str
    value: str
    correct: bool


@dataclass
class QuizQuestionStats:
    question_id: str
    body: str
    type: str
    points_possible: int
    scores: list[QuizQuestionAttempt]
    parts: list[QuizQuestionPart]
    difficulty = None
    discrimination = None
    per_part_stats = None


def process_quizzes(assignment, submissions, directory):
    body_ready, body = try_parse_file(assignment.instructions, "Quiz Body")
    checks_ready, checks = try_parse_file(assignment.on_run, "Quiz Checks")
    # TODO: Handle errors better
    if not body_ready and checks_ready:
        print("Error: instructions or on_run not valid", body, checks)
        return
    # Setup question information
    questions = {}
    checks = checks.get("questions", {})
    for question_id, question in body.get("questions", {}).items():
        # check = checks.get(question['id'], {})
        questions[question_id] = QuizQuestionStats(
            question_id=question_id,
            body=Markdown(extensions=["fenced_code"]).convert(question["body"]),
            type=question.get("type"),
            points_possible=question["points"],
            scores=[],
            parts=[],
        )
    # Iterate through submissions
    for submission in submissions:
        quiz_result = process_quiz_str(
            assignment.instructions, assignment.on_run, submission.code
        )
        if not quiz_result.graded_successfully:
            print("Error: quiz submission was not valid", quiz_result)
            continue
        # Attach the scores to the question
        feedbacks = quiz_result.feedbacks
        for question_id, feedback in feedbacks.items():
            questions[question_id].scores.append(
                QuizQuestionAttempt(
                    correct=feedback["correct"],
                    score=feedback["score"],
                    overall_score=quiz_result.score,
                )
            )
        if "studentAnswers" not in quiz_result.submission_body:
            print("Error: quiz submission did not have student answers")
            continue
        student_answers = quiz_result.submission_body["studentAnswers"]
        for question_id, student in student_answers.items():
            question = body.get("questions", {}).get(question_id, {})
            check = checks.get(question_id, {})
            feedback = feedbacks.get(question_id, {})
            keys, values, parts, s_answers = [], [], [], []
            if question.get("type") == "multiple_answers_question":
                for potential_answer in question["answers"]:
                    keys.append(potential_answer)
                    values.append(tuple(student))
                    parts.append(potential_answer)
            elif question.get("type") == "matching_question":
                for index, (statement, answer) in enumerate(
                    zip(question["statements"], student)
                ):
                    if isinstance(answer, list):
                        for sub_answer in answer:
                            keys.append(statement)
                            values.append(sub_answer)
                            parts.append(index)
                    else:
                        keys.append(statement)
                        values.append(answer)
                        parts.append(index)
            elif question.get("type") in (
                "multiple_dropdowns_question",
                "fill_in_multiple_blanks_question",
            ):
                for key, value in student.items():
                    keys.append(key)
                    values.append(value)
                    parts.append(key)
            else:
                keys, values, parts = [None], [student], [None]
            for key, value, part in zip(keys, values, parts):
                correctness = check_quiz_answer(
                    question, feedback, value, check, True, part
                )
                questions[question_id].parts.append(
                    QuizQuestionPart(
                        key=key,
                        value=(
                            ("Chosen" if part in value else "Not Chosen")
                            if question.get("type") == "multiple_answers_question"
                            else value
                        ),
                        correct=correctness,
                    )
                )
    # Post process for difficulty and discrimination
    for question_id, question in questions.items():
        if question.scores:
            question.difficulty = sum(score.score for score in question.scores) / len(
                question.scores
            )
        if len(question.scores) >= 2:
            question.discrimination = correlation(
                [score.overall_score for score in question.scores],
                [score.score for score in question.scores],
            )
        result = {}
        for part in question.parts:
            if part.key not in result:
                result[part.key] = {}
            if part.value not in result[part.key]:
                result[part.key][part.value] = []
            result[part.key][part.value].append(part.correct or False)
        scored = {}
        for key, values in result.items():
            scored[key] = {}
            for value, corrects in values.items():
                scored[key][value] = (
                    str(corrects[0]) if corrects else "Unknown",
                    len(corrects),
                    float(len(corrects)) / len(question.scores),
                    binconf(len(corrects), len(question.scores)),
                )
        question.per_part_stats = scored
    return questions
