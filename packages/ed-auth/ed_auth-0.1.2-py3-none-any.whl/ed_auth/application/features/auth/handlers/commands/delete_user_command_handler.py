from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_auth.application.common.responses.base_response import BaseResponse
from ed_auth.application.contracts.infrastructure.persistence.abc_unit_of_work import \
    ABCUnitOfWork
from ed_auth.application.features.auth.requests.commands import DeleteUserCommand
from ed_auth.common.exception_helpers import ApplicationException, Exceptions
from ed_auth.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(DeleteUserCommand, BaseResponse[None])
class DeleteUserCommandHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: DeleteUserCommand
    ) -> BaseResponse[None]:
        if self._uow.user_repository.get(id=request.id) is None:
            raise ApplicationException(Exceptions.NotFoundException, "User deletion failed.", ["User not found."])

        if not self._uow.user_repository.delete(request.id):
            raise ApplicationException(
                Exceptions.InternalServerException,
                "User deletion failed.",
                ["Internal server error."],
            )

        return BaseResponse[None].success(
            "User deleted successfully.",
            None,
        )

        
