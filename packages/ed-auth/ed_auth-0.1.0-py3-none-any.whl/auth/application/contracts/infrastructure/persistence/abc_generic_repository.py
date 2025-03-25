from abc import ABCMeta, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class ABCGenericRepository(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def get_all(self, **filters: Any) -> list[T]: ...

    @abstractmethod
    def get(self, **filters: Any) -> T | None: ...

    @abstractmethod
    def create(self, entity: T) -> T: ...

    @abstractmethod
    def update(self, id: UUID, entity: T) -> bool: ...

    @abstractmethod
    def delete(self, id: UUID) -> bool: ...
