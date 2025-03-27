from typing import Dict, Collection
from arq_base_python.cqrs.core_api.src.models.handler_registry import HandlerRegistry
from arq_base_python.cqrs.core_api.src.handlers.registered_event_handler import RegisteredEventHandler
from arq_base_python.cqrs.core_api.src.handlers.registered_command_handler import RegisteredCommandHandler


class HandlerResolver:
    def __init__(self, registries: Collection[HandlerRegistry]):
        self.event_listeners: Dict[str, RegisteredEventHandler] = {}
        self.command_handlers: Dict[str, RegisteredCommandHandler] = {}

        for handler in registries.get_event_listeners():
            self.event_listeners[handler.get_message_name()] = handler

        for handler in registries.get_command_handlers():
            self.command_handlers[handler.get_message_name()] = handler

    def get_command_handler(self, path: str) -> RegisteredCommandHandler:
        return self.command_handlers.get(path)

    def get_event_listener(self, path: str) -> RegisteredEventHandler:
        return self.event_listeners.get(path)

    def __repr__(self) -> str:
        return f"HandlerResolver({self.event_listeners}, {self.command_handlers})"
