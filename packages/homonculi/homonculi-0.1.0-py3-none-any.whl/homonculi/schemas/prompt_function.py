import re
from dataclasses import dataclass
from config import Configuration
import os
import difflib

from file_utilities import read_yaml_file


@dataclass
class PromptCollection:
    student_prompts: list[dict]
    question_format_prompt: dict
    feedback_format_prompt: dict

    def to_json(self):
        return {
            "student_prompts": self.student_prompts,
            "question_format_prompt": self.question_format_prompt,
            "feedback_format_prompt": self.feedback_format_prompt,
        }


def find_prompts(prompt_names: list[str], possible_prompts: dict[str, dict]):
    for prompt_name in prompt_names:
        if prompt_name in possible_prompts:
            yield possible_prompts[prompt_name]
        else:
            closest = difflib.get_close_matches(prompt_name, possible_prompts.keys())
            if closest:
                raise ValueError(
                    f"Could not find prompt with name: {prompt_name}. Did you mean: {closest[0]}?"
                )
            else:
                raise ValueError(f"Could not find any prompt with name: {prompt_name}")


def load_prompts(config: Configuration) -> PromptCollection:
    question_format = read_yaml_file(config.question_format_prompt_path)
    feedback_format = (
        read_yaml_file(config.feedback_format_prompt_path)
        if config.feedback_format_prompt_path
        else None
    )
    prompt_directories = config.student_prompt_dirs.split(";")
    # First try fast mode, if all the student prompts have .yaml extensions
    if all(
        student_prompt.endswith(".yaml") for student_prompt in config.student_prompts
    ):
        student_prompts = [
            read_yaml_file(student_prompt) for student_prompt in config.student_prompts
        ]
        return PromptCollection(student_prompts, question_format, feedback_format)
    # Search recursively for all prompt files (yaml file with metadata.name field)
    all_prompts = {}
    for prompt_dir in prompt_directories:
        for root, _, files in os.walk(prompt_dir):
            for file in files:
                if file.endswith(".yaml"):
                    prompt_data = read_yaml_file(os.path.join(root, file))
                    if "metadata" in prompt_data and "name" in prompt_data["metadata"]:
                        all_prompts[prompt_data["metadata"]["name"]] = prompt_data
    # Return just the matching prompts
    student_prompts = list(
        find_prompts(
            [p.strip() for p in config.student_prompts.split(",")], all_prompts
        )
    )
    return PromptCollection(student_prompts, question_format, feedback_format)


@dataclass
class PromptFunction:
    body: str
    function: dict

    def to_json(self):
        return {"body": self.body, "function": self.function}


def as_numbers(value):
    return list(range(len(value)))


SQUARE_BRACKETS = re.compile(r"(?<!\\)(\[.*?\]\]?)(?!\()")


def extract_blanks(body: str) -> list[str]:
    parts = SQUARE_BRACKETS.split(body)
    return [
        part[1:-1]
        for part in parts
        if not (part.startswith("[[") and part.endswith("]]"))
        and part.startswith("[")
        and part.endswith("]")
    ]


def make_prompt_for_question_type(
    question,
    student_prompt,
    question_prompt_parts,
    include_confidence,
):
    question_type = question["type"]
    qpp_for_type = question_prompt_parts[question_type]

    use_numeric = qpp_for_type.get("use_numeric", False)
    type_if_use_numeric = "number" if use_numeric else "string"
    enum_if_use_numeric = (
        as_numbers(question.get("answers", []))
        if use_numeric
        else question.get("answers", [])
    )

    if question_type == "short_answer_question":
        instructions = qpp_for_type["instructions"]
        prompt_question = {"type": "string", "description": qpp_for_type["description"]}

    elif question_type == "multiple_choice_question":
        instructions = "\n".join(
            [qpp_for_type["instructions"]]
            + [
                qpp_for_type["answer"].format(number=num, answer=a)
                for num, a in enumerate(question["answers"])
            ]
        )
        prompt_question = {
            "type": type_if_use_numeric,
            "enum": enum_if_use_numeric,
            "description": qpp_for_type["description"],
        }

    elif question_type == "true_false_question":
        instructions = qpp_for_type["instructions"]
        prompt_question = {
            "type": "string",
            "enum": qpp_for_type["true_false"],
            "description": qpp_for_type["description"],
        }

    elif question_type == "multiple_answers_question":
        instructions = "\n".join(
            [qpp_for_type["instructions"]]
            + [
                qpp_for_type["answer"].format(number=num, answer=a)
                for num, a in enumerate(question["answers"])
            ]
        )
        prompt_question = {
            "type": "array",
            "items": {
                "type": type_if_use_numeric,
                "enum": enum_if_use_numeric,
            },
            "description": qpp_for_type["description"],
        }

    elif question_type == "matching_question":
        instruction_parts = [qpp_for_type["instructions"]] + [
            qpp_for_type["statement"].format(statement=statement, number=num)
            for num, statement in enumerate(question["statements"])
        ]
        if qpp_for_type.get("show_answers_in_instructions", False):
            instruction_parts += [
                qpp_for_type["answer"].format(answer=answer, number=num)
                for num, answer in enumerate(question["answers"])
            ]
        instructions = "\n".join(instruction_parts)
        prompt_question = {
            "type": "array",
            "items": {"type": type_if_use_numeric, "enum": enum_if_use_numeric},
            "description": qpp_for_type["description"],
        }

    elif question_type == "fill_in_multiple_blanks_question":
        instructions = qpp_for_type["instructions"]
        # statements = [
        #     qpp_for_type["statement"].format(statement=statement, number=num)
        #     for num, statement in enumerate(question["statements"])
        # ]
        blanks = extract_blanks(question["body"])
        prompt_question = {
            "type": "object",
            "properties": {blank: {"type": "string"} for blank in blanks},
            "required": blanks,
            "description": qpp_for_type["description"],
            "additional_properties": False,
        }

    else:
        raise ValueError(f"Unknown question type: {question_type}")

    generic_question = question_prompt_parts["question"]

    parameters = {
        "type": "object",
        "properties": {"answer": prompt_question},
        "required": ["answer"],
        "additional_properties": False,
    }

    if include_confidence:
        word = question_prompt_parts["confidence"]["word"]
        parameters["properties"][word] = question_prompt_parts["confidence"]["settings"]
        parameters["required"].append(word)

    return PromptFunction(
        student_prompt["prompt"].format(
            body=generic_question["body"].format(body=question["body"]),
            instructions=generic_question["instructions"].format(
                instructions=instructions
            ),
        ),
        {
            "name": generic_question["name"],
            "description": generic_question["description"],
            "parameters": parameters,
        },
    )


def make_prompt_for_feedback(correct, feedback_prompt_parts):
    return PromptFunction(
        feedback_prompt_parts["prompt"].format(
            correctness="correct" if correct else "incorrect", correct=correct
        ),
        {
            "name": feedback_prompt_parts["name"],
            "description": feedback_prompt_parts["description"],
            "parameters": {
                "type": "object",
                "properties": feedback_prompt_parts["properties"],
                "required": list(feedback_prompt_parts["properties"]),
                "additional_properties": False,
            },
        },
    )
