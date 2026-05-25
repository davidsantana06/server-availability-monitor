from enum import Enum


class ServerStatus(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
