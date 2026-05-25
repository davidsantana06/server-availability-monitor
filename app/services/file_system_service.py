import json
from pathlib import Path
from typing import Any


def load_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return [stripped for line in file if (stripped := line.strip())]


def resolve_path(file_path: str) -> Path:
    path = Path(file_path)
    return path if path.is_absolute() else Path.cwd() / path
