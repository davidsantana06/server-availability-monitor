from dataclasses import dataclass
from ._base import Base


@dataclass(frozen=True)
class UsersInfo(Base):
    username: str
    email: str

    def validate(self) -> Base.DTOValidation:
        return self._aggregate([
            (self._is_not_blank(self.username), f"invalid username: {self.username!r}"),
            (self._is_email(self.email), f"invalid email: {self.email!r}"),
        ])
