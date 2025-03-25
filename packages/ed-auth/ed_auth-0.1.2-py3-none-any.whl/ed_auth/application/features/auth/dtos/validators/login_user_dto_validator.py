from ed_auth.application.features.auth.dtos.login_user_dto import LoginUserDto
from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class LoginUserDtoValidator(ABCDtoValidator[LoginUserDto]):
    def validate(self, dto: LoginUserDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the login user dto

        if dto.get("email") is None and dto.get("phone_number") is None:
            errors.append("Either email or phone number must be provided")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
