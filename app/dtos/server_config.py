from dataclasses import dataclass

from app.dtos._base import Base
from app.types import DtoValidation


@dataclass(frozen=True)
class ServerConfig(Base):
    hostname: str
    host: str
    port: int

    def __is_hostname_valid(self) -> bool:
        return isinstance(self.hostname, str) and len(self.hostname.strip()) > 0

    def __is_host_valid(self) -> bool:
        return isinstance(self.host, str) and len(self.host.strip()) > 0

    def __is_port_valid(self) -> bool:
        return (
            isinstance(self.port, int)
            and not isinstance(self.port, bool)
            and 1 <= self.port <= 65535
        )

    def validate(self) -> DtoValidation:
        return self._aggregate([
            (self.__is_hostname_valid(), f"invalid hostname: {self.hostname!r}"),
            (self.__is_host_valid(), f"invalid host: {self.host!r}"),
            (self.__is_port_valid(), f"invalid port: {self.port!r}"),
        ])
