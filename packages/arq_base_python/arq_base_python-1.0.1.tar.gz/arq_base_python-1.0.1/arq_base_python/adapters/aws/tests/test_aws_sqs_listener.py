import asyncio
import pytest
from faker import Faker
from unittest.mock import MagicMock
from boto3 import Session

from arq_base_python.adapters.aws.src.aws_sqs_listener import SqsListener
from unittest.mock import MagicMock, patch, AsyncMock
from botocore.exceptions import ClientError


fake = Faker()


@pytest.fixture()
def setup_session():
    return MagicMock(spec=Session)


@pytest.fixture()
def setup_sqs_listener(setup_session):
    return SqsListener(queue="", session=setup_session)


def test_setup(setup_sqs_listener):
    assert setup_sqs_listener


def test_initialize_client(setup_sqs_listener):
    assert setup_sqs_listener._initialize_client()


def test_parse_message_attributes(setup_sqs_listener):
    assert isinstance(setup_sqs_listener._parse_message_attributes(
        message_attributes={"attributes": {"one": "one"}}), dict)


def test_start(setup_sqs_listener):
    assert setup_sqs_listener.start_thread() is None


@pytest.fixture()
def setup_session():
    return MagicMock(spec=Session)


@pytest.fixture()
def setup_sqs_listener(setup_session):
    return SqsListener(queue="test_queue", session=setup_session, region_name="us-east-1")


def test_initialize_client(setup_sqs_listener):
    client = setup_sqs_listener._initialize_client()
    assert client is not None
    assert setup_sqs_listener._queue_url is not None


def test_initialize_client_with_error(setup_sqs_listener):
    setup_sqs_listener._session.client.return_value.get_queue_url.side_effect = ClientError(
        {'Error': {'Code': 'AWS.SimpleQueueService.NonExistentQueue'}}, 'GetQueueUrl')
    with pytest.raises(ClientError):
        setup_sqs_listener._initialize_client()


@pytest.mark.asyncio
async def test_start_sqs_listener_better(setup_sqs_listener):
    # Arrange
    with patch('aiobotocore.session.get_session', new_callable=MagicMock) as mock_get_session:
        mock_client = AsyncMock()
        mock_client.receive_message.return_value = {
            'Messages': [{'Body': 'test_body', 'MessageAttributes': {}, 'ReceiptHandle': 'test_receipt_handle'}]
        }
        mock_client.delete_message.return_value = {}
        mock_get_session.return_value.create_client.return_value.__aenter__.return_value = mock_client

        setup_sqs_listener.handle_message = MagicMock()

        # Agregar un contador para limitar el número de iteraciones
        max_iterations = 3
        iteration_count = 0
        stop_event = asyncio.Event()

        async def limited_receive_message(*args, **kwargs):
            nonlocal iteration_count
            if iteration_count < max_iterations:
                iteration_count += 1
                return {
                    'Messages': [{'Body': 'test_body', 'MessageAttributes': {}, 'ReceiptHandle': 'test_receipt_handle'}]
                }
            else:
                stop_event.set()
                return {'Messages': []}

        mock_client.receive_message.side_effect = limited_receive_message

        # Act
        await setup_sqs_listener._start_sqs_listener_better(stop_=stop_event)

        # Assert
        mock_client.receive_message.assert_called()
        setup_sqs_listener.handle_message.assert_called_with('test_body', {})
        mock_client.delete_message.assert_called_with(
            QueueUrl=setup_sqs_listener._queue_url,
            ReceiptHandle='test_receipt_handle'
        )


def test_parse_message_attributes(setup_sqs_listener):
    # Arrange
    message_attributes = {
        'Attribute1': {'StringValue': 'Value1'},
        'Attribute2': {'StringValue': 'Value2'}
    }

    # Act
    parsed_attributes = setup_sqs_listener._parse_message_attributes(
        message_attributes)

    # Assert
    assert parsed_attributes == {
        'Attribute1': 'Value1', 'Attribute2': 'Value2'}


def test_start_thread(setup_sqs_listener):
    # Act and Assert
    with patch('threading.Thread') as mock_thread:
        setup_sqs_listener.start_thread()
        mock_thread.assert_called_once()
        mock_thread.return_value.start.assert_called_once()
