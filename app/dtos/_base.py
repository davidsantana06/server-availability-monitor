from typing import NamedTuple


class Base:
    class DTOValidation(NamedTuple):
        is_valid: bool
        errors: str

    def _aggregate(self, validations: list[DTOValidation]) -> DTOValidation:
        errors = [msg for is_valid, msg in validations if not is_valid and msg]
        return Base.DTOValidation(not errors, "; ".join(errors))
