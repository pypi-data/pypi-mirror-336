from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.auth.application.features.auth.requests.commands import DeleteUserCommand
from src.auth.common.logging_helpers import get_logger
from src.auth.webapi.common.helpers import GenericResponse, rest_endpoint
from src.auth.webapi.dependency_setup import mediator

ROUTER = APIRouter(prefix="/users", tags=["Users"])
LOG = get_logger()


@ROUTER.delete("/{id}", response_model=GenericResponse[None])
@rest_endpoint
async def delete_user(
    id: UUID, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(DeleteUserCommand(id))

