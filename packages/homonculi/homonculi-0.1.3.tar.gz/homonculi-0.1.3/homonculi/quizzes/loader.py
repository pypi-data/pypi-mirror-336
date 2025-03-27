from pathlib import Path
import json
import yaml
import csv
from dataclasses import dataclass

from homonculi.config import Configuration
from homonculi.file_utilities import (
    chomp_extension,
    clean_filename,
    read_file,
    try_possible_extensions,
)
from homonculi.quizzes.questions import (
    QuizQuestion,
    convert_questions,
    extract_feedback,
    get_id,
)


@dataclass
class QuizFile:
    name: str
    questions: dict[str, QuizQuestion]
    pools: list[dict]
    settings: dict

    def __init__(self, name, questions, pools, settings):
        self.name = clean_filename(name)
        self.questions = convert_questions(questions)
        self.pools = pools
        self.settings = settings

    def to_json(self):
        return {
            "name": self.name,
            "questions": {q.id: q.to_json() for q in self.questions},
            "pools": self.pools,
            "settings": self.settings,
        }


def load_file(config: Configuration) -> QuizFile:
    if config.quiz_load_mode == "flat":
        return load_flat_file(
            read_file(config.quiz_path, config.quiz_load_format), config
        )
    elif config.quiz_load_mode == "spreadsheet":
        return load_spreadsheet_file(config.quiz_path, config)
    elif config.quiz_load_mode == "single":
        return load_single_quiz_file(
            read_file(config.quiz_path, config.quiz_load_format), config
        )
    elif config.quiz_load_mode == "split":
        return load_split_quiz_file(
            read_file(config.quiz_path, config.quiz_load_format),
            read_file(config.quiz_feedback_path, config.quiz_load_format),
            config,
        )
    elif config.quiz_load_mode == "guess":
        if Path(config.quiz_path).suffix == ".csv":
            return load_spreadsheet_file(config.quiz_path, config)
        else:
            data = read_file(config.quiz_path, config.quiz_load_format)
            if isinstance(data, list):
                return load_flat_file(data, config)
            elif config.quiz_feedback_path is not None:
                return load_split_quiz_file(
                    data,
                    read_file(config.quiz_feedback_path, config.quiz_load_format),
                    config,
                )
            else:
                return load_single_quiz_file(data, config)


def add_question(questions, pools, question_data):
    question_id = question_data["name"]
    # TODO: Handle if there is a pool field
    questions[question_id] = question_data


def load_flat_file(file_list: list[str], config: Configuration) -> QuizFile:
    quiz_name = config.quiz_path
    base_path = Path(config.quiz_path).parent
    questions, pools = {}, {}
    if not file_list:
        raise ValueError("No questions found in file list")
    if "header" in file_list[0].lower():
        file_list = file_list[1:]
        actual_path = try_possible_extensions(file_list[0], base_path)
        settings = read_file(actual_path, "guess")
    else:
        settings = {}
    for file_path in file_list:
        pool_name = chomp_extension(file_path)
        actual_path = try_possible_extensions(file_path, base_path)
        questions_data = read_file(actual_path, "guess")
        if isinstance(questions_data, dict) and "name" in questions_data:
            add_question(questions, pools, questions_data)
        elif len(questions_data) == 1:
            if isinstance(questions_data, dict):
                question_pool_id, question_data = list(questions_data.items())[0]
                question_data["name"] = question_pool_id
                add_question(questions, pools, question_data)
            elif isinstance(questions_data, list):
                add_question(questions, pools, questions_data[0])
            else:
                raise ValueError(
                    "Invalid question data (should be dict or list): "
                    + str(questions_data[0])
                )
        elif isinstance(questions_data, list):
            pools[pool_name] = []
            for index, question_data in enumerate(questions_data):
                add_question(questions, pools, question_data)
                pools[pool_name].append(get_id(question_data, index))
        elif isinstance(questions_data, dict):
            pools[pool_name] = []
            for question_pool_id, question_data in questions_data.items():
                question_data["name"] = question_pool_id
                add_question(questions, pools, question_data)
                pools[pool_name].append(question_pool_id)
    return QuizFile(quiz_name, questions, pools, settings)


def load_single_quiz_file(contents: dict | list, config: Configuration) -> QuizFile:
    if isinstance(contents["questions"], dict):
        if "feedback" in contents:
            feedback = contents.pop("feedback")
            for question_id, question_data in contents["questions"].items():
                # TODO: Fire a warning if question has no feedback
                question_data.update(extract_feedback(feedback.get(question_id, {})))
                question_data["name"] = question_id
        else:
            for question_id, question_data in contents["questions"].items():
                question_data["name"] = question_id
        return QuizFile(
            contents.get("name", config.quiz_path),
            contents.get("questions", {}),
            contents.get("pools", []),
            contents.get("settings", {}),
        )
    else:
        contents["questions"] = {
            get_id(q, i): q for i, q in enumerate(contents["questions"])
        }
        return QuizFile(
            contents.get("name", config.quiz_path),
            contents["questions"],
            contents.get("pools", []),
            contents.get("settings", {}),
        )


def load_split_quiz_file(
    questions: dict, feedback: dict, config: Configuration
) -> QuizFile:
    if isinstance(questions["questions"], dict):
        for question_id, question_data in questions["questions"].items():
            # TODO: Fire a warning if question has no feedback
            check = extract_feedback(feedback["questions"].get(question_id, {}))
            question_data.update(check)
            question_data["name"] = question_id
        return QuizFile(
            questions.get("name", config.quiz_path),
            questions["questions"],
            questions.get("pools", []),
            questions.get("settings", {}),
        )
    else:
        questions["questions"] = {q["name"]: q for q in questions["questions"]}
        return QuizFile(
            config.quiz_path,
            questions["questions"],
            questions.get("pools", []),
            questions.get("settings", {}),
        )


def load_spreadsheet_file(file_path: str, config: Configuration) -> QuizFile:
    raise NotImplementedError("Spreadsheet loading not yet implemented")
