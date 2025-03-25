from abc import ABCMeta

from ed.domain.entities.otp import Otp

from src.auth.application.contracts.infrastructure.persistence.abc_generic_repository import \
    ABCGenericRepository


class ABCOtpRepository(
    ABCGenericRepository[Otp],
    metaclass=ABCMeta,
): ...
