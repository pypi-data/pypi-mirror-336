import shlex
from dataclasses import dataclass
import simple_parsing
from simple_parsing.helpers import Serializable


@dataclass
class Configuration(Serializable):

    quiz_path: str
    """The path to the quiz file. If it's a txt file, then it should be a list of relative paths to actual questions. Yaml/JSON file can either be a list of relative paths, or the actual questions (in the documented Quiz structure)."""

    quiz_feedback_path: str | None = None
    """If given, this is assumed to be the autograding logic of the JSON, separate from the quiz questions stored in quiz_path."""

    attempts: int = 3
    """The number of times to ask the LLM to solve each quiz question. """

    quiz_load_mode: str = "guess"
    """The mode to use to load the quiz file. Can be 'guess', 'flat', 'single', 'split', or 'spreadsheet'."""

    quiz_load_format: str = "guess"
    """The format to use to load the quiz file. Can be 'guess', 'json', 'yaml', 'txt', or 'csv'."""

    output_format: str = "both"
    """The format to use to output the results. Can be 'csv', 'log', or 'both'."""

    output_dir: str = "results"
    """The directory to save the results to. """

    results_path: str = "{quiz}_{time}.csv"
    """The path template to save the results to. Can use {quiz} and {time} as placeholders."""

    log_path: str = "{quiz}_{time}.yml"
    """The path template to save the log to. Can use {quiz} and {time} as placeholders."""

    seed: int = 42
    """The seed to use for the random number generator (not on GPT, just locally). """

    backup_save_threshold: int = 60 * 2
    """The number of seconds between each backup save; useful for long runs. """

    ask_for_feedback_on_answer: bool = True
    """Whether to ask the LLM for feedback on the feedback. """

    include_confidence: bool = True
    """Whether to include the confidence in the output. """

    student_prompt_dirs: str = "./prompts/students/"
    """A semicolon-separated list of directories containing student prompt files. """

    student_prompts: str = "./prompts/students/default.yaml"
    """A comma-separated list of student prompt files to use; matches the filename if an extension is present, otherwise uses the internal name in the prompt file (searching through the student_prompt_dirs). """

    question_format_prompt_path: str = "./prompts/questions/default.yaml"
    """The path to the question format prompt file; this will be used to construct the actual question function. """

    feedback_format_prompt_path: str = "./prompts/feedback/default.yaml"
    """The path to the feedback format prompt file; this will be used to construct the feedback on grading function. """

    gpt_api_key_path: str = "./openai_key.txt"
    """The path to the file containing the API key for OpenAI's API. """

    gpt_api_key: str | None = None
    """The API key for OpenAI's API. """

    gpt_model: str = "gpt-4o-mini"
    """The model to use for the GPT API. """

    gpt_temperature: float = 0.5
    """The temperature to use for the GPT API; controls some of the randomness. """

    gpt_top_p: float = 0.9
    """ The top_p value to use for the GPT API; controls the diversity of the output. """

    gpt_max_tokens: int = 1000
    """The maximum number of tokens to generate for the GPT API. """


def parse_configuration(args=None):
    parser = simple_parsing.ArgumentParser(add_config_path_arg=True)

    parser.add_arguments(Configuration, dest="config")

    if isinstance(args, str):
        args = shlex.split(args)

    return parser.parse_args(args)
