from app.dtos import UserInfo
from app.services import file_system_service
from app.types import RawUserInfo


_user_infos = []


def load(file_path: str) -> list[UserInfo]:
    global _user_infos
    data = file_system_service.load_json(file_path)
    _user_infos = [_map_as_dto(item) for item in data]
    return _user_infos


def get_all() -> list[UserInfo]:
    return _user_infos


def _map_as_dto(raw_user_info: RawUserInfo) -> UserInfo:
    return UserInfo(**raw_user_info)
