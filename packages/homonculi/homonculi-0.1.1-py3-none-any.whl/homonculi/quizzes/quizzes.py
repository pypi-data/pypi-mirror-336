import os
import re
from pprint import pprint
import sys
import json
from dataclasses import dataclass

from quizzes.questions import check_quiz_question
from text_utilities import compare_string_equality


@dataclass
class QuizResult:
    score: float
    correct: bool
    points_possible: int
    feedbacks: dict[str, str]
    graded_successfully: bool
    submission_body: dict
    error: str


def try_parse_file(contents: str, filename: str):
    try:
        return True, json.loads(contents)
    except json.JSONDecodeError as e:
        return False, f"No JSON could be parsed from {filename}.\n{str(e)}"


def process_quiz_str(body: str, checks: str, submission_body: str) -> QuizResult:
    """(status, correct, score, points, feedbacks, submission_body)"""
    body_ready, body = try_parse_file(body, "Quiz Body")
    checks_ready, checks = try_parse_file(checks, "Quiz Checks")
    student_ready, student = try_parse_file(
        submission_body or "{}", "Student Submission"
    )
    if not body_ready:
        return QuizResult(0, 0, 0, {}, False, None, body)
    if not checks_ready:
        return QuizResult(0, 0, 0, {}, False, None, checks)
    if not student_ready:
        return QuizResult(0, 0, 0, {}, False, None, student)
    return process_quiz(body, checks, student)


def process_quiz(body: dict, checks: dict, submission_body: dict) -> QuizResult:
    # Extract the requisite data within the objects
    student_answers = submission_body.get("studentAnswers", {})
    checks = checks.get("questions", {})
    questions = body.get("questions", {})
    # For each question in the on_run, run the evaluation criteria
    total_score, total_points = 0.0, 0.0
    total_correct = True
    feedbacks = {}
    for question_id, question in questions.items():
        student = student_answers.get(question_id)
        if student is None:
            # Hack - for now we just skip missing student submissions
            continue
        check = checks.get(question_id, {})
        points = question.get("points", 1)
        total_points += points
        checked_question = check_quiz_question(question, check, student)
        if checked_question is None:
            feedbacks[question_id] = {
                "message": "Unknown Type: " + question.get("type"),
                "correct": None,
                "score": 0,
                "status": "error",
            }
        else:
            score, correct, feedback = checked_question
            # print(question_id, score)
            total_score += score * points
            total_correct = total_correct and correct
            message = str(feedback)
            feedbacks[question_id] = {
                "message": message,
                "correct": correct,
                "score": score,
                "status": "graded",
            }
    # Report back the final score and feedback objects
    # print(total_score, total_points)
    return QuizResult(
        total_score / total_points if total_points else 0,
        total_correct,
        total_points,
        feedbacks,
        True,
        submission_body,
        None,
    )
