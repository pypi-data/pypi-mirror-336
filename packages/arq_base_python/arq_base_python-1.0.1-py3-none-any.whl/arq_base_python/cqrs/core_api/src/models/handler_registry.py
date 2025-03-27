from typing import List, Type, TypeVar
from arq_base_python.cqrs.core_api.src.models.event import Event
from arq_base_python.cqrs.core_api.src.models.command import Command
from arq_base_python.cqrs.core_api.src.handlers.message_handler import MessageHandler
from arq_base_python.cqrs.core_api.src.handlers.registered_event_handler import RegisteredEventHandler
from arq_base_python.cqrs.core_api.src.handlers.registered_command_handler import RegisteredCommandHandler

T = TypeVar('T')


class HandlerRegistry:
    def __init__(self):
        self._event_listeners: List[RegisteredEventHandler] = []
        self._command_handlers: List[RegisteredCommandHandler] = []

    @staticmethod
    def register():
        return HandlerRegistry()

    def handle_command(self, command_name: str, handler: MessageHandler[Command[T], Event], command_class: Type[T]):
        self._command_handlers.append(RegisteredCommandHandler(
            command_name, handler, command_class))
        return self

    def listen_event(self, event_name: str, handler: MessageHandler[Event[T], Event], event_class: Type[T]):
        self._event_listeners.append(
            RegisteredEventHandler(event_name, handler, event_class))
        return self

    def get_event_listeners(self) -> List[RegisteredEventHandler]:
        return self._event_listeners

    def get_command_handlers(self) -> List[RegisteredCommandHandler]:
        return self._command_handlers
