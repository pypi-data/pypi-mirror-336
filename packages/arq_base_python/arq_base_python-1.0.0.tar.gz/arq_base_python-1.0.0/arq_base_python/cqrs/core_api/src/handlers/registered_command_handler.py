from typing import TypeVar, Type
from cqrs.core_api.src.handlers.message_handler import MessageHandler
from cqrs.core_api.src.handlers.registered_handler import RegisteredHandler
from cqrs.core_api.src.models.event import Event
from cqrs.core_api.src.models.command import Command

T = TypeVar('T')


class RegisteredCommandHandler(RegisteredHandler[Command[T], T]):
    def __init__(self, command_name: str, handler: MessageHandler[Command[T], Event], input_class: Type[T]):
        super().__init__(command_name, handler, input_class)

    def __repr__(self) -> str:
        return f"RegisteredCommandHandler({self.message_name}, {self.handler}, {self.input_class})"
