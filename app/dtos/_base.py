from typing import Any, NamedTuple
import re


class Base:
    _EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    DTOValidation = NamedTuple("DTOValidation", [('is_valid', bool), ('errors', str)])

    def _aggregate(self, validations: list[DTOValidation]) -> DTOValidation:
        errors = [msg for is_valid, msg in validations if not is_valid and msg]
        return self.DTOValidation(not errors, "; ".join(errors))

    @staticmethod
    def _is_bool(v: Any) -> bool:
        return isinstance(v, bool)

    @staticmethod
    def _is_positive_int(v: Any) -> bool:
        return isinstance(v, int) and not isinstance(v, bool) and v > 0

    @staticmethod
    def _is_int_in_range(v: Any, min_value: int, max_value: int) -> bool:
        return isinstance(v, int) and not isinstance(v, bool) and min_value <= v <= max_value

    @classmethod
    def _is_port(cls, v: Any) -> bool:
        return cls._is_positive_int(v) and 1 <= v <= 65535

    @staticmethod
    def _is_not_blank(v: str) -> bool:
        return isinstance(v, str) and bool(v.strip())

    @staticmethod
    def _is_non_empty(v: str) -> bool:
        return isinstance(v, str) and len(v) > 0

    @classmethod
    def _is_email(cls, v: str) -> bool:
        return isinstance(v, str) and cls._EMAIL_REGEX.match(v) is not None
