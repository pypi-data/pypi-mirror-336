from src.auth.application.contracts.infrastructure.persistence.abc_user_repository import \
    ABCUserRepository
from src.auth.infrastructure.persistence.db_client import DbClient
from src.auth.infrastructure.persistence.repositories.generic_repository import \
    GenericRepository
from ed.domain.entities import User


class UserRepository(GenericRepository[User], ABCUserRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "user")
