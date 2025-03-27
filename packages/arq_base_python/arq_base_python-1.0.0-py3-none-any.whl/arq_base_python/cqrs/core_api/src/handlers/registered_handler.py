from typing import TypeVar, Generic, Type
from cqrs.core_api.src.handlers.message_handler import MessageHandler
from cqrs.core_api.src.models.event import Event

# Definir las restricciones genéricas
T = TypeVar('T', bound='CommonBody')
E = TypeVar('E')


class RegisteredHandler(Generic[T, E]):
    def __init__(self, message_name: str, handler: MessageHandler[T, Event], input_class: Type[E]):
        self.message_name = message_name
        self.handler = handler
        self.input_class = input_class

    def get_message_name(self) -> str:
        return self.message_name

    def get_handler(self) -> MessageHandler[T, Event]:
        return self.handler

    def get_input_class(self) -> Type[E]:
        return self.input_class
