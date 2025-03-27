"""

A few different ways to use this:

```shell
python simulate.py --quiz_path
```

Quizzes can be provided:
- As a single JSON file
- As a split JSON file with questions and autograding code
- As a collection of YAML files including an index.yaml
- As a remote canvas identifier using Waltz

The simulator will:
- Run in immediate mode
- Run in batch mode

The output will be:
- A CSV file with the results
- A detailed log file with the prompts and runs

By default, the system will send two queries per question:
- First, it will ask GPT to answer the question
- Second, it will show GPT its feedback, and ask for a response

You can override any part of the prompting:
- The student prompt
- The question format prompt
- The feedback format prompt

You can also override the GPT model and parameters.
"""

from pprint import pprint
import sys
import time
import random
import copy
import csv
from dataclasses import dataclass
import yaml
from tqdm import tqdm
from tqdm.contrib import itertools
from collections import defaultdict
import json
from pathlib import Path

from homonculi.config import Configuration, parse_configuration
from homonculi.file_utilities import add_to_csv, backup_log, start_csv
from homonculi.job import RESULT_HEADERS, JobData, ResultRow
from homonculi.quizzes.questions import QuizQuestion, post_process_answer
from homonculi.quizzes.quizzes import check_quiz_question
from homonculi.quizzes.loader import load_file
from homonculi.openai_api import OpenAI
import homonculi.quizzes as quizzes
from homonculi.schemas.prompt_function import (
    PromptFunction,
    load_prompts,
    make_prompt_for_feedback,
)
from homonculi.schemas.prompt_function import make_prompt_for_question_type
import logging

logger = logging.getLogger("homunculi")


def simulate_students(config: Configuration):
    """
    Simulate student working on a quiz
    """
    logger.info("Starting simulation")
    quiz = load_file(config)
    prompts = load_prompts(config)
    job = JobData(config, quiz, prompts)
    grader = OpenAI(config)

    store_results = config.output_format in ["both", "csv"]
    store_logs = config.output_format in ["both", "log"]
    if store_results:
        result_path = config.results_path.format(quiz=quiz.name, time=job.time_started)
        result_path = Path(config.output_dir) / result_path
        start_csv(result_path, RESULT_HEADERS)
    if store_logs:
        log_path = config.log_path.format(quiz=quiz.name, time=job.time_started)
        log_path = Path(config.output_dir) / log_path
        backup_log(job, log_path)
    last_dumped_log = time.time()

    estimated_total = (
        len(quiz.questions) * len(prompts.student_prompts) * config.attempts
    )
    progress_bar = tqdm(
        itertools.product(
            quiz.questions, prompts.student_prompts, range(config.attempts)
        ),
        total=estimated_total,
    )  # smooth=0.1

    if config.seed:
        random.seed(config.seed)

    for question, student_prompt, attempt_id in progress_bar:
        student_id = student_prompt["metadata"]["name"]
        progress_bar.set_description(f"{question.id}/{student_id}/{attempt_id}")
        created_student_prompt = make_prompt_for_question_type(
            question,
            student_prompt,
            prompts.question_format_prompt,
            config.include_confidence,
        )
        # Record the prompt if it is new
        if question.id not in job.created_prompts:
            job.created_prompts[question.id] = {}
        if student_id not in job.created_prompts[question.id]:
            job.created_prompts[student_id] = created_student_prompt.to_json()

        # Make the actual chat completion and submit to GPT
        # TODO: Allow the user to provide context (e.g., previous question, group question)
        conversation = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": created_student_prompt.body},
                ],
            }
        ]
        potential_images = question.get_images()
        if potential_images:
            for image in potential_images:
                conversation[0]["content"].append(
                    {"type": "image_file", "image_url": image}
                )
        result, full_result = grader.run_function(
            conversation, created_student_prompt.function
        )
        answer = post_process_answer(
            question, result["answer"], prompts.question_format_prompt
        )
        if answer.system_error:
            logger.error(answer.system_error)
            continue

        # Check the answer
        score, correct, feedback = check_quiz_question(
            question, question["check"], answer.answer
        )

        row = ResultRow(
            question.id,
            student_id,
            attempt_id,
            answer.answer if answer.system_error is None else answer.original_answer,
            result.get("confidence", ""),
            score,
            correct,
            question.points,
            score * question.points,
            answer.system_error or "",
            feedback,
            "",
            "",
        )
        # Handle checking the question
        if config.ask_for_feedback_on_answer:
            created_feedback_prompt = make_prompt_for_feedback(
                correct, prompts.feedback_format_prompt
            )
            conversation.append(
                {"role": "system", "content": created_feedback_prompt.body}
            )
            feedback, full_feedback = grader.run_function(
                conversation, created_feedback_prompt.function
            )
            row.mistake = feedback["mistake"]
            row.reason = feedback["reason"]

        if store_results:
            add_to_csv(result_path, row.to_csv(config.include_confidence))

        if store_logs:
            dumped_model = full_result.model_dump()
            dumped_model["prompt"] = copy.deepcopy(conversation)
            job.runs.append(dumped_model)

        time_passed = time.time() - last_dumped_log

        if time_passed > config.backup_save_threshold:
            logger.info(f"Time passed: {time_passed} seconds. Saving log.")
            progress_bar.set_description("Saving log...")

            backup_log(job, log_path)
            last_dumped_log = time.time()

    job.time_finished = int(time.time())

    if store_logs:
        backup_log(job, log_path)


def main():
    config = parse_configuration(sys.argv[1:])
    simulate_students(config)


if __name__ == "__main__":
    main()
