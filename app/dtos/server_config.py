from dataclasses import dataclass
from ._base import Base


@dataclass(frozen=True)
class ServerConfig(Base):
    hostname: str
    host: str
    port: int

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (self._is_not_blank(self.hostname), f"invalid hostname: {self.hostname!r}"),
            (self._is_not_blank(self.host), f"invalid host: {self.host!r}"),
            (self._is_port(self.port), f"invalid port: {self.port!r}"),
        ])
