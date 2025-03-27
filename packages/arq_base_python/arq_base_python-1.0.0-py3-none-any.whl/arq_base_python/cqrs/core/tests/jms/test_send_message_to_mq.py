from cqrs.core_api.src.event.event_error import EventError
from datetime import date
from unittest import mock
from unittest.mock import MagicMock

import pytest
from faker import Faker

from cqrs.core.src.jms.send_message_to_mq import SendMessageToMQ
from cqrs.core_api.src.messaging.message_serializer import MessageSerializer
from cqrs.core.src.properties.developer_mode_props import DeveloperModeProps
from cqrs.core.src.jms.properties_creator import PropertiesCreator
from cqrs.core_api.src.models.command_submitted import CommandSubmitted
from cqrs.core_api.src.models.event_submitted import EventSubmitted
from cqrs.core_api.src.properties.destinations import Destinations
from cqrs.core_api.src.jms.concrete_sender import ConcreteSender
from cqrs.core_api.src.models.command import Command
from cqrs.core_api.src.models.event import Event


fake = Faker()


@pytest.fixture()
def setup_serializer():
    return MagicMock(spec=MessageSerializer)


@pytest.fixture()
def setup_developer_mode_props():
    return DeveloperModeProps()


@pytest.fixture()
def setup_properties_creator(setup_developer_mode_props):
    return PropertiesCreator(
        developer_node_props=setup_developer_mode_props
    )


@pytest.fixture()
def setup_mq_destinations():
    return MagicMock(spec=Destinations)


@pytest.fixture()
def setup_sender():
    return MagicMock(spec=ConcreteSender)


@pytest.fixture()
def setup_send_message_to_mq(setup_properties_creator, setup_mq_destinations, setup_serializer, setup_sender):
    return SendMessageToMQ(
        properties_creator=setup_properties_creator,
        mq_destinations=setup_mq_destinations,
        serializer=setup_serializer,
        sender=setup_sender
    )


@pytest.fixture()
def setup_command():
    command = Command()
    return command


@pytest.fixture()
def setup_event():
    event = Event()
    return event


@pytest.mark.asyncio
async def test_publish(setup_send_message_to_mq, setup_command):
    assert await setup_send_message_to_mq.publish(pubmsg=setup_command) is None


def test_parse_event(setup_send_message_to_mq, setup_event):
    assert isinstance(setup_send_message_to_mq._parse_to_submittable(
        pubmsg=setup_event), EventSubmitted)


def test_parse_command(setup_send_message_to_mq, setup_command):
    assert isinstance(setup_send_message_to_mq._parse_to_submittable(
        pubmsg=setup_command), CommandSubmitted)


@pytest.mark.asyncio
async def test_publish_error(setup_send_message_to_mq, setup_command):
    # Arrange
    message = '{"comando":{"id":"83985d89-aaf3-4009-ac15-e5460c4cc079","nombre":"task.error"},"validationStatus":0,"validationMessage":null}'
    extract_id_mock = MagicMock(
        return_value="83985d89-aaf3-4009-ac15-e5460c4cc079")
    setup_send_message_to_mq._extract_id = extract_id_mock

    # Act
    assert await setup_send_message_to_mq.publishError(message=message, errorMSG="Error") is None

    # Assert
    extract_id_mock.assert_called_once_with(message)


def test_extract_message_data(setup_send_message_to_mq, setup_command):
    r = setup_send_message_to_mq._extract_msg_data(pubmsg=setup_command)
    assert isinstance(r, tuple)
    assert r[0] == "Comando"


@pytest.fixture
def serializer():
    return mock.create_autospec(MessageSerializer)


@pytest.fixture
def send_message_to_mq(serializer):
    return SendMessageToMQ(None, None, None, serializer)


def test_parse_to_event_error_from_command(send_message_to_mq, serializer):
    # Arrange: Preparamos un CommandSubmitted y su objeto de Command asociado
    command = Command(id="123", nombre="TestCommand", dni=None)
    command_submitted = CommandSubmitted(command)
    serializer.serialize.return_value = '{"key": "value"}'

    # Act: Llamamos al método privado usando name mangling
    event_error = send_message_to_mq._SendMessageToMQ__parse_to_event_error_from_command(
        command_submitted)

    # Assert: Verificamos que los campos se hayan asignado correctamente
    assert isinstance(event_error, EventError)
    assert event_error.uuid == "123"
    assert event_error.name == "TestCommand"
    assert event_error.json == '{"key": "value"}'
    assert event_error.fechaEvento == date.today().strftime('%Y-%m-%d')
    assert event_error.clase == "COMANDO"
    assert event_error.dni is None  # Como no tiene DNI, debería ser None


def test_parse_to_event_error_from_event(send_message_to_mq, serializer):
    # Arrange: Preparamos un EventSubmitted y su objeto de Event asociado
    event = Event(id="456", nombre="TestEvent", dni=None)
    event_submitted = EventSubmitted(event)

    serializer.serialize.return_value = '{"eventKey": "eventValue"}'

    # Act: Llamamos al método privado usando name mangling
    event_error = send_message_to_mq._SendMessageToMQ__parse_to_event_error_from_event(
        event_submitted)

    # Assert: Verificamos que los campos se hayan asignado correctamente
    assert isinstance(event_error, EventError)
    assert event_error.uuid == "456"
    assert event_error.name == "TestEvent"
    assert event_error.json == '{"eventKey": "eventValue"}'
    assert event_error.fechaEvento == date.today().strftime('%Y-%m-%d')
    assert event_error.clase == "EVENTO"
    assert event_error.dni is None  # Como no tiene DNI, debería ser None


def test_parse_to_event_error(send_message_to_mq):
    # Arrange: Preparamos un CommandSubmitted y un EventSubmitted
    command = Command(id="123", nombre="TestCommand", dni=None)
    command_submitted = CommandSubmitted(command)

    # Act: Llamamos al método privado para un comando
    event_error = send_message_to_mq._SendMessageToMQ__parse_to_event_error(
        command_submitted)

    # Assert: Verificamos que se haya llamado correctamente para Command
    assert isinstance(event_error, EventError)
    assert event_error.uuid == "123"
    assert event_error.clase == "COMANDO"

    # Arrange: Preparamos un EventSubmitted
    event = Event(id="456", nombre="TestEvent", dni=None)
    event_submitted = EventSubmitted(event)

    # Act: Llamamos al método privado para un evento
    event_error_event = send_message_to_mq._SendMessageToMQ__parse_to_event_error(
        event_submitted)

    # Assert: Verificamos que se haya llamado correctamente para Event
    assert isinstance(event_error_event, EventError)
    assert event_error_event.uuid == "456"
    assert event_error_event.clase == "EVENTO"

    # Arrange: Usamos un objeto inválido (ni Command ni Event)
    with pytest.raises(Exception, match="El objeto a convertir no es ni comando ni evento"):
        send_message_to_mq._SendMessageToMQ__parse_to_event_error(
            "invalid_object")
