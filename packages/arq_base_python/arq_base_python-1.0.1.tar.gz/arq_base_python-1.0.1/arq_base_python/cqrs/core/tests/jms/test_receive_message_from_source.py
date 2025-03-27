import pytest
import uuid
from faker import Faker
from unittest.mock import MagicMock
from reactivex import of, operators as op

from arq_base_python.cqrs.core.src.jms.receive_message_from_source import ReceiveMessageFromSource
from arq_base_python.cqrs.core.src.jms.send_message_to_mq import SendMessageToMQ
from arq_base_python.cqrs.core.src.properties.developer_mode_props import DeveloperModeProps
from arq_base_python.cqrs.core.src.jms.properties_creator import PropertiesCreator

from arq_base_python.cqrs.core_api.src.properties.destinations import Destinations
from arq_base_python.cqrs.core_api.src.jms.concrete_sender import ConcreteSender
from arq_base_python.cqrs.core_api.src.messaging.message_serializer import MessageSerializer
from arq_base_python.cqrs.core_api.src.jms.base_message import BaseMessage
from arq_base_python.cqrs.core_api.src.models.received_message import ReceivedMessage
from arq_base_python.cqrs.core.src.jms.async_executor_service import AsyncExecutorService
from arq_base_python.jano.core.src.secured_application import SecuredApplication
from arq_base_python.cqrs.core.src.handlers.handler_resolver import HandlerResolver


fake = Faker()


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
def setup_serializer():
    return MagicMock(spec=MessageSerializer)


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
def setup_secured_application():
    return MagicMock(spec=SecuredApplication)


@pytest.fixture()
def setup_handler_resolver():
    return MagicMock(spec=HandlerResolver)


@pytest.fixture()
def setup_async_executor_service(setup_serializer, setup_secured_application, setup_send_message_to_mq, setup_handler_resolver):
    return AsyncExecutorService(
        serializer=setup_serializer,
        secured_application=setup_secured_application,
        send_message_to_mq=setup_send_message_to_mq,
        handler_resolver=setup_handler_resolver
    )


@pytest.fixture()
def setup_receive_message_from_source(setup_send_message_to_mq, setup_async_executor_service):
    return ReceiveMessageFromSource(send_message_to_mq=setup_send_message_to_mq, async_executor_service=setup_async_executor_service)


@pytest.fixture()
def setup_base_message():
    base_message = BaseMessage(
        body={"one": "two"},
        messageId=str(uuid.uuid4()),
        headers={
            "one": "two",
            # "type": "TYPE-DESCONOCIDO",
            # "type": "COMMAND",
            # "type": "EVENT",
            # "type": "LOG"
        }
    )
    return base_message


def test_process_message(setup_receive_message_from_source, setup_base_message):
    setup_receive_message_from_source.processMessage(var1=setup_base_message)


@pytest.fixture()
def setup_reactive_base_message(setup_base_message):
    return of(setup_base_message)


def test_process_receive_base_message(setup_receive_message_from_source, setup_reactive_base_message):
    assert setup_receive_message_from_source.receive_base_message(
        var1=setup_reactive_base_message)


def test_parse(setup_receive_message_from_source, setup_reactive_base_message):
    assert isinstance(setup_receive_message_from_source.parse(mqMessage=setup_reactive_base_message.run()),
                      ReceivedMessage)


@pytest.mark.asyncio
async def test_filter_base_message(setup_receive_message_from_source, setup_reactive_base_message):
    assert setup_receive_message_from_source.filter_base_message(
        received_message=setup_receive_message_from_source.parse(mqMessage=setup_reactive_base_message.run())) == False
