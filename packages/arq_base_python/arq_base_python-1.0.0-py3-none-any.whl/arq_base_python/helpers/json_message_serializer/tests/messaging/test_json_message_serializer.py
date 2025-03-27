import json
import uuid
from unittest.mock import MagicMock

import pytest
from faker import Faker

from cqrs.core_api.src.models.command_submitted import CommandSubmitted
from cqrs.core_api.src.models.event_submitted import EventSubmitted
from helpers.json_message_serializer.src.messaging.json_message_serializer import JsonMessageSerializer
from cqrs.core_api.src.models.command import Command
from cqrs.core_api.src.models.received_message import ReceivedMessage


fake = Faker()


@pytest.fixture()
def setup_json_message_serializer():
    return JsonMessageSerializer()


@pytest.fixture()
def setup_command():
    command = Command()
    return command


def test_serialize(setup_json_message_serializer):
    assert isinstance(setup_json_message_serializer.serialize(
        var1={"test": "test_one"}), str)


def test_serialize_submittable(setup_json_message_serializer, setup_command):
    assert isinstance(setup_json_message_serializer.serialize_submittable(
        var1=setup_command), str)


def test_parse_payload_dict(setup_json_message_serializer):
    # Arrange
    payload = {"key": "value"}

    # Act
    result = setup_json_message_serializer.parse_payload(payload, dict)

    # Assert
    assert isinstance(result, dict)
    assert result == payload


def test_parse_payload_object(setup_json_message_serializer):
    # Arrange
    class TestObject:
        def __init__(self, key):
            self.key = key

    payload = {"key": "value"}

    # Act
    result = setup_json_message_serializer.parse_payload(payload, TestObject)

    # Assert
    assert isinstance(result, TestObject)
    assert result.key == "value"


def test_parse_payload_invalid(setup_json_message_serializer):
    # Arrange
    payload = "invalid_payload"

    # Act & Assert
    with pytest.raises(Exception, match="Error parsing payload"):
        setup_json_message_serializer.parse_payload(payload, dict)


def test_to_command_submitted(setup_json_message_serializer):
    # Arrange
    command_data = {
        "comando": {"nombre": "test_command"},
        "validationStatus": 1,
        "validationMessage": "Valid"
    }
    command_json = json.dumps(command_data)

    # Act
    result = setup_json_message_serializer.to_command_submitted(command_json)

    # Assert
    assert isinstance(result, CommandSubmitted)
    assert result.get().nombre == "test_command"
    assert result.get_validation_status() == 1
    assert result.get_validation_message() == "Valid"


def test_to_event_submitted(setup_json_message_serializer):
    # Arrange
    event_data = {
        "evento": {"nombre": "test_event"},
        "validationStatus": 1,
        "validationMessage": "Valid"
    }
    event_json = json.dumps(event_data)

    # Act
    result = setup_json_message_serializer.to_event_submitted(event_json)

    # Assert
    assert isinstance(result, EventSubmitted)
    assert result.get().nombre == "test_event"
    assert result.get_validation_status() == 1
    assert result.get_validation_message() == "Valid"
