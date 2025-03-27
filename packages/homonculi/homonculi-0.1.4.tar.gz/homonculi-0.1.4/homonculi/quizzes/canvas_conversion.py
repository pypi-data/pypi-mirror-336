from pprint import pprint
import sys
import os
import json


def convert_quiz_question(question) -> tuple[dict, dict]:
    """

    :param question:
    :return: (body, checks)
    """
    body, check = {}, {}
    body["id"] = question["question_name"]
    body["type"] = question["question_type"]
    body["points"] = question["points_possible"]
    body["body"] = question["question_text"]
    check["id"] = question["question_name"]
    if question.get("incorrect_comments_html"):
        check["wrong_any"] = question.get("incorrect_comments_html")
    # Actual per-question handling
    if question["question_type"] == "true_false_question":
        answers = question["answers"]
        for answer in answers:
            check["correct"] = (answer["text"] == "True") == (answer["weight"] == 100)
            if answer.get("comments"):
                check["wrong"] = answer.get("comments")
    elif question["question_type"] == "matching_question":
        answers = [statement["left"] for statement in question["answers"]]
        answers.extend(
            [
                text
                for text in (
                    question.get("matching_answer_incorrect_matches") or ""
                ).split("\n")
                if text
            ]
        )
        body["answers"] = answers
        body["statements"] = [answer["text"] for answer in question["matches"]]
        check["correct"] = {
            statement["right"]: statement["left"] for statement in question["answers"]
        }
        check["wrong"] = {
            statement.get("comments", "") for statement in question["answers"]
        }
    elif question["question_type"] == "multiple_choice_question":
        body["answers"] = [answer["text"] for answer in question["answers"]]
        check["correct"] = [
            statement["text"]
            for statement in question["answers"]
            if statement["weight"] == 100
        ][0]
        check["feedback"] = {
            statement["text"]: statement["comments"]
            for statement in question["answers"]
            if statement["weight"] == 0 and statement.get("comments")
        }
    elif question["question_type"] == "multiple_answers_question":
        if question["question_name"] == "DetermineAppropriateDataFlow":
            pprint(question)
        body["answers"] = [
            answer.get("html", answer.get("text")) for answer in question["answers"]
        ]
        check["correct"] = [
            statement.get("html", statement.get("text"))
            for statement in question["answers"]
            if statement["weight"] == 100
        ]
        # TODO: Shouldn't I utilize these comments?
    elif question["question_type"] == "multiple_dropdowns_question":
        answers = [answer["text"] for answer in question["answers"]]
        answers.extend(
            [
                text
                for text in (
                    question.get("matching_answer_incorrect_matches") or ""
                ).split("\n")
                if text
            ]
        )
        body["answers"] = {
            statement["blank_id"]: answers for statement in question["answers"]
        }
        check["correct"] = {
            statement["blank_id"]: statement["text"]
            for statement in question["answers"]
        }
        check["wrong"] = {
            statement["blank_id"]: statement["comments"]
            for statement in question["answers"]
            if statement.get("comments")
        }
    elif question["question_type"] == "short_answer_question":
        check["correct_exact"] = [
            statement["text"] for statement in question["answers"]
        ]
    elif question["question_type"] == "numerical_question":
        pprint(question)
        # TODO: Find one
    elif question["question_type"] == "fill_in_multiple_blanks_question":
        check["correct"] = {}
        for answer in question["answers"]:
            blank_id = answer["blank_id"]
            if blank_id not in check["correct"]:
                check["correct"][blank_id] = []
            check["correct"][blank_id].append(answer["text"])
    return body, check


def clean_name(filename):
    # TODO: Make this more robust, like secure_filename from Werkzeug
    return filename.replace(" ", "_").replace("-", "_").replace("__", "_")


if __name__ == "__main__":
    # TODO: Rewrite this to use argparse
    # TODO: Add a flag to specify the output directory
    # TODO: Get rid of sneks references
    # TODO: Give some code to actually connect and get quiz from Canvas
    if len(sys.args) < 2:
        raise ValueError(
            "Too few arguments to the script: provide `filename` to the canvas quiz files"
        )
    all_json_path = sys.args[2]
    with open(all_json_path) as all_json_file:
        all_json = json.load(all_json_file)
    all_done = []
    for quiz in sorted(all_json, key=lambda x: x["title"]):
        print(quiz["title"])
        body, checks = {"questions": {}}, {"questions": {}}
        for question in quiz["questions"]:
            body_item, checks_item = convert_quiz_question(question)
            body["questions"][body_item.pop("id")] = body_item
            checks["questions"][checks_item.pop("id")] = checks_item
        # pprint(body)
        # pprint(checks)
        folder_name = "sneks_" + clean_name(quiz["title"] + "_quiz")
        try:
            os.makedirs(f"sneks_quizzes/{folder_name}")
        except FileExistsError:
            pass
        with open(rf"sneks_quizzes/{folder_name}/index.md", "w") as index_file:
            json.dump(body, index_file, indent=2)
        with open(rf"sneks_quizzes/{folder_name}/on_run.py", "w") as on_run_file:
            json.dump(checks, on_run_file, indent=2)
        for touchee in ["on_eval.py", "starting_code.py"]:
            with open(rf"sneks_quizzes/{folder_name}/{touchee}", "w") as touched:
                pass
