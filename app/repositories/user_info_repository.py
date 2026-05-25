from app.dtos import UserInfo
from app.services import file_system_service


_user_infos = []


def load(file_path: str) -> list[UserInfo]:
    global _user_infos
    data = file_system_service.load_json(file_path)
    _user_infos = [_map(item) for item in data]
    return _user_infos


def get_all() -> list[UserInfo]:
    return _user_infos


def _map(item: dict) -> UserInfo:
    return UserInfo(
        username=item["username"],
        email=item["email"],
    )
