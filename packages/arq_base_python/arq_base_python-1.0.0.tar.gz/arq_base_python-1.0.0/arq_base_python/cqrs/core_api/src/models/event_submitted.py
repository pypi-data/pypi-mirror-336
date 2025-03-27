from dataclasses import dataclass, field
from typing_extensions import Annotated

from cqrs.core_api.src.models.event import Event
from cqrs.core_api.src.models.submittable import Submittable


class EventSubmitted(Submittable[Event]):
    def __init__(
        self,
        evento: Event = Event(),
        validation_status: int = 0,
        validation_message: str = None,
    ) -> None:
        self.__evento = evento
        self.__validation_status = validation_status
        self.__validation_message = validation_message

    def get(self) -> Event:
        return self.__evento

    def get_validation_status(self) -> int:
        return self.__validation_status

    def set_validation_status(self, validation_status: int):
        self.__validation_status = validation_status

    def get_validation_message(self) -> str:
        return self.__validation_message

    def set_validation_message(self, validation_message: str):
        self.__validation_message = validation_message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(evento={self.get()}, validation_status={self.get_validation_status()}, validation_message={self.get_validation_message()})"

    def __dict__(self) -> dict:
        return {
            "evento": self.get(),
            "validationStatus": self.get_validation_status(),
            "validationMessage": self.get_validation_message(),
        }
