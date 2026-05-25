import re
from dataclasses import dataclass

from app.dtos._base import Base
from app.types import DtoValidation


_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class UserInfo(Base):
    username: str
    email: str

    def __is_username_valid(self) -> bool:
        return isinstance(self.username, str) and len(self.username.strip()) > 0

    def __is_email_valid(self) -> bool:
        return isinstance(self.email, str) and _EMAIL_REGEX.match(self.email) is not None

    def validate(self) -> DtoValidation:
        return self._aggregate([
            (self.__is_username_valid(), f"invalid username: {self.username!r}"),
            (self.__is_email_valid(), f"invalid email: {self.email!r}"),
        ])
