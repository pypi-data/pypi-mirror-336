from dataclasses import dataclass
from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T", bound="CommonBody")


class Submittable(ABC, Generic[T]):

    @abstractmethod
    def get(self) -> T:
        pass

    @abstractmethod
    def get_validation_status(self) -> int:
        pass

    @abstractmethod
    def set_validation_status(self, validation_status: int) -> None:
        pass

    @abstractmethod
    def get_validation_message(self) -> str:
        pass

    @abstractmethod
    def set_validation_message(self, validation_message: str) -> None:
        pass
