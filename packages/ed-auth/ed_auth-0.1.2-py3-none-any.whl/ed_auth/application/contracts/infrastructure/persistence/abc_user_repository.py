from abc import ABCMeta

from ed_domain.entities import User

from ed_auth.application.contracts.infrastructure.persistence.abc_generic_repository import \
    ABCGenericRepository


class ABCUserRepository(
    ABCGenericRepository[User],
    metaclass=ABCMeta,
): ...
