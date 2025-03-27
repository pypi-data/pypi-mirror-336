import yaml
import csv
import json
from pathlib import Path
import os
import frontmatter


def start_csv(output_path: str, header):
    """
    Start a csv file with a header
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)


def add_to_csv(output_path: str, row):
    """
    Add feedback to a csv file
    """
    with open(output_path, "a", newline="", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(row)


def backup_log(info, meta_path: str):
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)
    with open(meta_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(info.to_json(), f)


def chomp_extension(file_path: str) -> str:
    return Path(file_path).with_suffix("").name


def clean_filename(file_path: str) -> str:
    return Path(file_path).with_suffix("").name


def try_possible_extensions(file_path: str, base_path: str) -> str:
    for ext in ["", ".yaml", ".json", ".txt", ".md"]:
        possible = (Path(base_path) / file_path).with_suffix(f"{ext}")
        if possible.exists():
            return str(possible)
    raise ValueError(
        "Could not find file with any valid extensions (json, yaml, txt, md): "
        + file_path
    )


def read_md_file(file_path: str) -> dict | list[str]:
    with open(file_path) as f:
        data = frontmatter.load(f)
        return [line.strip("- *\t") for line in data.content.split("\n")]


def read_json_file(file_path: str) -> dict | list[str]:
    with open(file_path) as f:
        return json.load(f)


def read_yaml_file(file_path: str) -> dict | list[str]:
    with open(file_path) as f:
        return yaml.safe_load(f)


def read_txt_file(file_path: str) -> list[str]:
    with open(file_path) as f:
        return [line.strip() for line in f.readlines()]


def read_file(file_path: str, file_format: str) -> dict | list[str]:
    if file_format == "json":
        return read_json_file(file_path)
    elif file_format == "yaml":
        return read_yaml_file(file_path)
    elif file_format == "txt":
        return read_txt_file(file_path)
    elif file_format == "md":
        return read_md_file(file_path)
    elif file_format == "guess":
        if file_path.endswith(".json"):
            return read_json_file(file_path)
        elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
            return read_yaml_file(file_path)
        elif file_path.endswith(".txt"):
            return read_txt_file(file_path)
        elif file_path.endswith(".md"):
            return read_md_file(file_path)
        else:
            raise ValueError("Could not guess file format")
    else:
        raise ValueError("Invalid file format")
