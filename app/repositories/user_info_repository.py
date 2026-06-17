from typing import TypedDict

from app.dtos import UsersInfo
from app.services import file_system_service


_RawUserInfo = TypedDict("_RawUserInfo", {"username": str, "email": str})


_user_infos = []


def load(file_path: str) -> list[UsersInfo]:
    global _user_infos
    raw_user_infos = file_system_service.load_json(file_path)
    _user_infos = [_map_as_dto(rui) for rui in raw_user_infos]
    return _user_infos


def get_all() -> list[UsersInfo]:
    return _user_infos


def _map_as_dto(raw_user_info: _RawUserInfo) -> UsersInfo:
    return UsersInfo(**raw_user_info)
