from ed_auth.application.features.auth.dtos import CreateUserDto
from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class CreateUserDtoValidator(ABCDtoValidator[CreateUserDto]):
    def validate(self, dto: CreateUserDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the login user dto

        if not dto["first_name"]:
            errors.append("First name is required")

        if not dto["last_name"]:
            errors.append("Last name is required")

        if not dto["password"]:
            errors.append("Password is required")

        if dto.get("email") is None and dto.get("phone_number") is None:
            errors.append("Either email or phone number must be provided")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
