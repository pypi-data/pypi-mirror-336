import argparse
import shlex
from dataclasses import dataclass, asdict, fields, field
from typing import Optional
from homonculi.file_utilities import read_yaml_file


@dataclass
class Configuration:
    quiz_path: str = field(
        metadata={
            "help": "The path to the quiz file. If it's a txt file, then it should be a list of relative paths to actual questions. Yaml/JSON file can either be a list of relative paths, or the actual questions (in the documented Quiz structure)."
        }
    )

    quiz_feedback_path: Optional[str] = field(
        default=None,
        metadata={
            "help": "If given, this is assumed to be the autograding logic of the JSON, separate from the quiz questions stored in quiz_path."
        },
    )
    attempts: int = field(
        default=3,
        metadata={
            "help": "The number of times to ask the LLM to solve each quiz question."
        },
    )
    quiz_load_mode: str = field(
        default="guess",
        metadata={
            "help": "The mode to use to load the quiz file. Can be 'guess', 'flat', 'single', 'split', or 'spreadsheet'."
        },
    )
    quiz_load_format: str = field(
        default="guess",
        metadata={
            "help": "The format to use to load the quiz file. Can be 'guess', 'json', 'yaml', 'txt', or 'csv'."
        },
    )
    output_format: str = field(
        default="both",
        metadata={
            "help": "The format to use to output the results. Can be 'csv', 'log', or 'both'."
        },
    )
    output_dir: str = field(
        default="results", metadata={"help": "The directory to save the results to."}
    )
    results_path: str = field(
        default="{quiz}_{time}.csv",
        metadata={
            "help": "The path template to save the results to. Can use {quiz} and {time} as placeholders."
        },
    )
    log_path: str = field(
        default="{quiz}_{time}.yml",
        metadata={
            "help": "The path template to save the log to. Can use {quiz} and {time} as placeholders."
        },
    )
    seed: int = field(
        default=42,
        metadata={
            "help": "The seed to use for the random number generator (not on GPT, just locally)."
        },
    )
    backup_save_threshold: int = field(
        default=60 * 2,
        metadata={
            "help": "The number of seconds between each backup save; useful for long runs."
        },
    )
    ask_for_feedback_on_answer: bool = field(
        default=False,
        metadata={"help": "Whether to ask the LLM for feedback on the feedback."},
    )
    include_confidence: bool = field(
        default=False,
        metadata={"help": "Whether to include the confidence in the output."},
    )
    student_prompt_dirs: str = field(
        default="./prompts/students/",
        metadata={
            "help": "A semicolon-separated list of directories containing student prompt files."
        },
    )
    student_prompts: str = field(
        default="./prompts/students/default.yaml",
        metadata={
            "help": "A comma-separated list of student prompt files to use; matches the filename if an extension is present, otherwise uses the internal name in the prompt file (searching through the student_prompt_dirs)."
        },
    )
    question_format_prompt_path: str = field(
        default="./prompts/questions/default.yaml",
        metadata={
            "help": "The path to the question format prompt file; this will be used to construct the actual question function."
        },
    )
    feedback_format_prompt_path: str = field(
        default="./prompts/feedback/default.yaml",
        metadata={
            "help": "The path to the feedback format prompt file; this will be used to construct the feedback on grading function."
        },
    )
    gpt_api_key_path: str = field(
        default="./openai_key.txt",
        metadata={
            "help": "The path to the file containing the API key for OpenAI's API."
        },
    )
    gpt_api_key: Optional[str] = field(
        default=None, metadata={"help": "The API key for OpenAI's API."}
    )
    gpt_model: str = field(
        default="gpt-4o-mini", metadata={"help": "The model to use for the GPT API."}
    )
    gpt_temperature: float = field(
        default=0.5,
        metadata={
            "help": "The temperature to use for the GPT API; controls some of the randomness."
        },
    )
    gpt_top_p: float = field(
        default=0.9,
        metadata={
            "help": "The top_p value to use for the GPT API; controls the diversity of the output."
        },
    )
    gpt_max_tokens: int = field(
        default=1000,
        metadata={"help": "The maximum number of tokens to generate for the GPT API."},
    )

    def to_json(self):
        return asdict(self)


def parse_configuration(args=None):
    parser = argparse.ArgumentParser(description="Quiz configuration")

    parser.add_argument("--config_path", type=str, help="Path to YAML config file")

    # Dynamically add fields from the Configuration dataclass
    for field_name, field_def in Configuration.__dataclass_fields__.items():
        arg_type = field_def.type if field_def.type != Optional[str] else str
        default = (
            field_def.default
            if field_def.default is not field_def.default_factory
            else None
        )
        help_text = field_def.metadata.get("help", "")

        if isinstance(default, bool):
            parser.add_argument(
                f"--{field_name}",
                action="store_true" if not default else "store_false",
                help=help_text,
            )
        else:
            parser.add_argument(
                f"--{field_name}",
                type=arg_type,
                default=argparse.SUPPRESS,
                help=help_text,
            )

    if isinstance(args, str):
        args = shlex.split(args)

    parsed_args = vars(parser.parse_args(args))

    config_path = parsed_args.pop("config_path", None)
    config_data = {}

    if config_path:
        config_data = read_yaml_file(config_path)

    for ignorable_default_bool in ["ask_for_feedback_on_answer", "include_confidence"]:
        if (
            ignorable_default_bool in parsed_args
            and parsed_args[ignorable_default_bool] is False
        ):
            del parsed_args[ignorable_default_bool]

    # Merge CLI args on top of config file
    all_args = {**config_data, **parsed_args}

    print(all_args)

    if "quiz_path" not in all_args:
        raise ValueError("You must provide a quiz_path parameter.")

    return Configuration(**all_args)
