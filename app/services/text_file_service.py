def read_lines(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return [stripped for line in file if (stripped := line.strip())]
