from app.types import DtoValidation


class Base:
    def _aggregate(self, validations: list[DtoValidation]) -> DtoValidation:
        errors = [msg for is_valid, msg in validations if not is_valid and msg]
        return not errors, "; ".join(errors)
