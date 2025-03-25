from typing import Any, Generic, TypeVar
from uuid import UUID

from ed_auth.application.contracts.infrastructure.persistence.abc_generic_repository import \
    ABCGenericRepository
from ed_auth.common.exception_helpers import ApplicationException, Exceptions
from ed_auth.common.logging_helpers import get_logger
from ed_auth.infrastructure.persistence.db_client import DbClient
from ed_auth.infrastructure.persistence.helpers import repository_class

TEntity = TypeVar("TEntity")

LOG = get_logger()


@repository_class
class GenericRepository(Generic[TEntity], ABCGenericRepository[TEntity]):
    def __init__(self, db: DbClient, collection: str) -> None:
        try:
            self._db = db.get_collection(f"{collection}s")
            self._collection = f"{collection[0].upper()}{collection[1:].lower()}"
        except Exception as e:
            LOG.error(f"Error initializing {self._collection} repository: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Error initializing repository.",
                [str(e)],
            )

    def get_all(self, **filters: Any) -> list[TEntity]:
        try:
            return list(self._db.find(filters))
        except Exception as e:
            LOG.error(f"Error retrieving all {self._collection} entities: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Error retrieving entities.",
                [str(e)],
            )

    def get(self, **filters: Any) -> TEntity | None:
        try:
            if entity := self._db.find_one(filters):
                return entity

            return None
        except Exception as e:
            LOG.error(f"Error retrieving {self._collection} entity: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException, "Error retrieving entity.", [
                    str(e)]
            )

    def create(self, entity: TEntity) -> TEntity:
        try:
            if exists := self._db.find_one(entity):
                raise ApplicationException(
                    Exceptions.BadRequestException,
                    message=f"{self._collection} already exists.",
                    errors=[f"{self._collection}: {exists} already exists"],
                )

            self._db.insert_one(entity)
            return entity
        except Exception as e:
            LOG.error(f"Error creating {self._collection} entity: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException, "Error creating entity.", [
                    str(e)]
            )

    def update(self, id: UUID, entity: TEntity) -> bool:
        try:
            status = self._db.update_one({"id": id}, {"$set": entity})
            return status.modified_count > 0
        except Exception as e:
            LOG.error(
                f"Error updating {self._collection} entity with id {id}: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException, "Error updating entity.", [
                    str(e)]
            )

    def delete(self, id: UUID) -> bool:
        try:
            status = self._db.delete_one({"id": id})
            return status.deleted_count > 0
        except Exception as e:
            LOG.error(
                f"Error deleting {self._collection} entity with id {id}: {e}")
            raise ApplicationException(
                Exceptions.InternalServerException, "Error deleting entity.", [
                    str(e)]
            )
