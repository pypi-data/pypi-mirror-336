import pytest
from unittest.mock import MagicMock
from arq_base_python.cqrs.core.src.handlers.handler_resolver import HandlerResolver
from arq_base_python.cqrs.core_api.src.models.handler_registry import HandlerRegistry
from arq_base_python.cqrs.core_api.src.handlers.registered_event_handler import RegisteredEventHandler
from arq_base_python.cqrs.core_api.src.handlers.registered_command_handler import RegisteredCommandHandler


@pytest.fixture
def handler_registry():
    registry = MagicMock(spec=HandlerRegistry)
    event_handler = MagicMock(spec=RegisteredEventHandler)
    event_handler.get_message_name.return_value = "event_name"
    command_handler = MagicMock(spec=RegisteredCommandHandler)
    command_handler.get_message_name.return_value = "command_name"
    registry.get_event_listeners.return_value = [event_handler]
    registry.get_command_handlers.return_value = [command_handler]
    return registry


@pytest.fixture
def handler_resolver(handler_registry):
    return HandlerResolver(handler_registry)


def test_init(handler_resolver):
    assert "event_name" in handler_resolver.event_listeners
    assert "command_name" in handler_resolver.command_handlers


def test_get_command_handler(handler_resolver):
    handler = handler_resolver.get_command_handler("command_name")
    assert handler is not None
    assert handler.get_message_name() == "command_name"


def test_get_command_handler_not_found(handler_resolver):
    handler = handler_resolver.get_command_handler("non_existent_command")
    assert handler is None


def test_get_event_listener(handler_resolver):
    listener = handler_resolver.get_event_listener("event_name")
    assert listener is not None
    assert listener.get_message_name() == "event_name"


def test_get_event_listener_not_found(handler_resolver):
    listener = handler_resolver.get_event_listener("non_existent_event")
    assert listener is None


def test_repr(handler_resolver):
    repr_str = repr(handler_resolver)
    assert "event_name" in repr_str
    assert "command_name" in repr_str
