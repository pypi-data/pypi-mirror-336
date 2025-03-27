from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from reactivex import Observable

# Define el tipo genérico T
T = TypeVar('T', bound='SQLModel')


class ReactiveCrud(ABC, Generic[T]):
    @abstractmethod
    def all(self) -> Observable[T]:
        """Returns all the elements as an Observable (similar to Flux in Java)."""
        pass

    @abstractmethod
    def save(self, entity: T) -> Observable[T]:
        """Saves the entity and returns the saved entity as an Observable."""
        pass

    @abstractmethod
    def update(self, entity: T) -> Observable[T]:
        """Updates the entity and returns the updated entity as an Observable."""
        pass

    @abstractmethod
    def delete(self, var1: int) -> Observable:
        """Deletes an entity by id and returns a completed Observable (Mono<Void> equivalent)."""
        pass
