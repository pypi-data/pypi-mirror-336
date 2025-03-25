from abc import ABCMeta

from ed_domain.entities.otp import Otp

from ed_auth.application.contracts.infrastructure.persistence.abc_generic_repository import \
    ABCGenericRepository


class ABCOtpRepository(
    ABCGenericRepository[Otp],
    metaclass=ABCMeta,
): ...
