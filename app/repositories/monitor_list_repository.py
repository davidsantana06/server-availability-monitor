from app.services import text_file_service


_hostnames = []


def load(file_path: str) -> list[str]:
    global _hostnames
    _hostnames = text_file_service.read_lines(file_path)
    return _hostnames


def get_all() -> list[str]:
    return _hostnames
