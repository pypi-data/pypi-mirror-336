import pytest
from faker import Faker
from unittest.mock import MagicMock
from boto3 import Session

from adapters.aws.src.aws_sns_init import AwsSNSInit
from adapters.aws.src.receive_message_from_sqs import ReceiveMessageFromSQS
from adapters.aws.src.config.aws_config import AwsListenerConfig


fake = Faker()


@pytest.fixture()
def setup_session():
    return MagicMock(spec=Session)


@pytest.fixture()
def setup_aws_sns_init():
    return MagicMock(spec=AwsSNSInit)


@pytest.fixture()
def setup_receive_message_from_sqs():
    return MagicMock(spec=ReceiveMessageFromSQS)


@pytest.fixture()
def setup_aws_config(setup_receive_message_from_sqs, setup_aws_sns_init):
    return AwsListenerConfig(sqs_init=setup_aws_sns_init, listener=setup_receive_message_from_sqs)


def test_setup(setup_aws_config):
    assert isinstance(setup_aws_config, AwsListenerConfig)


def test_get_listener(setup_aws_config):
    assert isinstance(setup_aws_config.get_listener(), ReceiveMessageFromSQS)
