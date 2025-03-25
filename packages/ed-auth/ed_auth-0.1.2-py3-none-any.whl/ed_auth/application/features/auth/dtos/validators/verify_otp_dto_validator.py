from ed_auth.application.features.auth.dtos.create_user_verify_dto import \
    CreateUserVerifyDto
from ed_auth.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)


class VerifyOtpDtoValidator(ABCDtoValidator[CreateUserVerifyDto]):
    def validate(self, dto: CreateUserVerifyDto) -> ValidationResponse:
        errors = []

        otp: str = dto["otp"]
        if len(otp) != 4:
            errors.append("OTP must be 4 numbers.")

        if otp.isnumeric() is False:
            errors.append("OTP must be numeric.")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
