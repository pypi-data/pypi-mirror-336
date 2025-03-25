from ed_domain.entities import User

from ed_auth.application.contracts.infrastructure.persistence.abc_user_repository import \
    ABCUserRepository
from ed_auth.infrastructure.persistence.db_client import DbClient
from ed_auth.infrastructure.persistence.repositories.generic_repository import \
    GenericRepository


class UserRepository(GenericRepository[User], ABCUserRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "user")
