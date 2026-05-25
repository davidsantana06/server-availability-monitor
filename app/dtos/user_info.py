import re
from dataclasses import dataclass

from app.types import DtoValidation


_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class UserInfo:
    username: str
    email: str

    def __is_username_valid(self) -> bool:
        return isinstance(self.username, str) and len(self.username.strip()) > 0

    def __is_email_valid(self) -> bool:
        return isinstance(self.email, str) and _EMAIL_REGEX.match(self.email) is not None

    def validate(self) -> DtoValidation:
        errors = []
        if not self.__is_username_valid():
            errors.append(f"invalid username: {self.username!r}")
        if not self.__is_email_valid():
            errors.append(f"invalid email: {self.email!r}")
        return (not errors, "; ".join(errors) or None)
