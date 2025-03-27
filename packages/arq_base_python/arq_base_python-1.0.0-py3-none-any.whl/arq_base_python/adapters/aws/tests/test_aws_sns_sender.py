import pytest
from faker import Faker
from unittest.mock import MagicMock
from boto3 import Session
from aioboto3.session import Session as AsyncSession

from adapters.aws.src.aws_sns_sender import AwsSnsSender
from cqrs.core_api.src.jms.base_message import BaseMessage


fake = Faker()


@pytest.fixture()
def setup_base_message():
    return MagicMock(spec=BaseMessage)


@pytest.fixture()
def setup_session():
    return MagicMock(spec=Session)


@pytest.fixture()
def setup_async_session():
    return MagicMock(spec=AsyncSession)


@pytest.fixture()
def setup_aws_sns_sender(setup_session, setup_async_session):
    aws_sns_sender = AwsSnsSender(aws_session=setup_session,
                                  async_session=setup_async_session)
    return aws_sns_sender


@pytest.mark.asyncio
async def test_send(setup_aws_sns_sender, setup_base_message):
    assert await setup_aws_sns_sender.send(
        destination="", base_message=setup_base_message) is None


def test_get_topic(setup_aws_sns_sender):
    assert setup_aws_sns_sender._get_topic(name="")


def test_create_message_attributes(setup_aws_sns_sender):
    assert setup_aws_sns_sender._create_message_attributes(
        attributes={"attribute": "one"})


def test_publish_message(setup_aws_sns_sender):
    topic = setup_aws_sns_sender._get_topic(name="")
    assert setup_aws_sns_sender.publish_message(message="",
                                                attributes={"attribute": "one"})
