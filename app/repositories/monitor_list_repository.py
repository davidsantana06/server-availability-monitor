from app.services import file_system_service


_hostnames = []


def load(file_path: str) -> list[str]:
    global _hostnames
    _hostnames = file_system_service.read_lines(file_path)
    return _hostnames


def get_all() -> list[str]:
    return _hostnames
