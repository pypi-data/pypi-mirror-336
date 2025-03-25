from datetime import UTC, datetime

from ed_domain.entities.otp import OtpVerificationAction
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from ed_auth.application.contracts.infrastructure.utils.abc_otp import ABCOtp
from ed_auth.application.contracts.infrastructure.utils.abc_password import \
    ABCPassword
from ed_auth.application.features.auth.dtos.unverified_user_dto import \
    UnverifiedUserDto
from ed_auth.application.features.auth.dtos.validators.login_user_dto_validator import \
    LoginUserDtoValidator
from ed_auth.application.features.auth.requests.commands.login_user_command import \
    LoginUserCommand
from ed_auth.common.exception_helpers import ApplicationException, Exceptions
from ed_auth.common.generic_helpers import get_new_id
from ed_auth.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(LoginUserCommand, BaseResponse[UnverifiedUserDto])
class LoginUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, otp: ABCOtp, password: ABCPassword):
        self._uow = uow
        self._otp = otp
        self._password = password

    async def handle(
        self, request: LoginUserCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        dto_validator = LoginUserDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Login failed.",
                dto_validator.errors,
            )

        email, phone_number = request.dto.get("email", ""), request.dto.get(
            "phone_number", ""
        )
        user = (
            self._uow.user_repository.get(email=email)
            if email
            else self._uow.user_repository.get(phone_number=phone_number)
        )

        if not user:
            raise ApplicationException(
                Exceptions.NotFoundException,
                "Login failed.",
                ["No user found with the given credentials."],
            )

        if user["password"]:
            if "password" not in request.dto:
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    "Login failed.",
                    ["Password is required."],
                )

            if not self._password.verify(request.dto["password"], user["password"]):
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    "Login failed.",
                    ["Password is incorrect."],
                )

        self._uow.otp_repository.create(
            {
                "id": get_new_id(),
                "user_id": user["id"],
                "action": OtpVerificationAction.LOGIN,
                "create_datetime": datetime.now(UTC),
                "expiry_datetime": datetime.now(UTC),
                "value": self._otp.generate(),
            }
        )

        return BaseResponse[UnverifiedUserDto].success(
            "Otp sent successfully.",
            UnverifiedUserDto(**user),  # type: ignore
        )
