from datetime import UTC, datetime

from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_domain.entities.otp import OtpVerificationAction
from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from ed_auth.application.contracts.infrastructure.utils.abc_otp import ABCOtp
from ed_auth.application.contracts.infrastructure.utils.abc_password import \
    ABCPassword
from ed_auth.application.features.auth.dtos import UnverifiedUserDto
from ed_auth.application.features.auth.dtos.validators import \
    CreateUserDtoValidator
from ed_auth.application.features.auth.requests.commands import \
    CreateUserCommand
from ed_auth.common.exception_helpers import ApplicationException, Exceptions
from ed_auth.common.generic_helpers import get_new_id
from ed_auth.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateUserCommand, BaseResponse[UnverifiedUserDto])
class CreateUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork, otp: ABCOtp, password: ABCPassword):
        self._uow = uow
        self._otp = otp
        self._password = password

    async def handle(
        self, request: CreateUserCommand
    ) -> BaseResponse[UnverifiedUserDto]:
        dto_validator = CreateUserDtoValidator().validate(request.dto)

        if not dto_validator.is_valid:
            raise ApplicationException(
                Exceptions.ValidationException,
                "Creating account failed.",
                dto_validator.errors,
            )

        dto = request.dto
        user = self._uow.user_repository.create(
            {
                "id": get_new_id(),
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto.get("email", ""),
                "phone_number": dto.get("phone_number", ""),
                "password": self._password.hash(dto["password"]),
                "verified": False,
                "create_datetime": datetime.now(UTC),
                "update_datetime": datetime.now(UTC),
            }
        )

        self._uow.otp_repository.create(
            {
                "id": get_new_id(),
                "user_id": user["id"],
                "action": OtpVerificationAction.VERIFY_EMAIL,
                "create_datetime": datetime.now(UTC),
                "expiry_datetime": datetime.now(UTC),
                "value": self._otp.generate(),
            }
        )

        return BaseResponse[UnverifiedUserDto].success(
            "Otp sent successfully.",
            UnverifiedUserDto(**user),  # type: ignore
        )
