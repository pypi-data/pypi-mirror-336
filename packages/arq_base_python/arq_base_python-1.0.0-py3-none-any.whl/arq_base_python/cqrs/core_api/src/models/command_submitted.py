from cqrs.core_api.src.models.command import Command
from cqrs.core_api.src.models.submittable import Submittable


class CommandSubmitted(Submittable[Command]):

    def __init__(
        self,
        comando: Command = None,
        validation_status: int = 0,
        validation_message: str = None,
    ):
        self.__comando = comando
        self.__validation_status = validation_status
        self.__validation_message = validation_message

    def get(self) -> Command:
        return self.__comando

    def get_validation_status(self) -> int:
        return self.__validation_status

    def set_validation_status(self, validation_status: int):
        self.__validation_status = validation_status

    def get_validation_message(self) -> str:
        return self.__validation_message

    def set_validation_message(self, validation_message: str):
        self.__validation_message = validation_message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(comando={self.get()}, validationStatus={self.get_validation_status()}, validationMessage={self.get_validation_message()})"

    def __dict__(self) -> dict:
        return {
            "comando": self.get().__dict__(),
            "validationStatus": self.get_validation_status(),
            "validationMessage": self.get_validation_message(),
        }
