import pytest
from faker import Faker
from unittest.mock import MagicMock

from arq_base_python.adapters.aws.src.aws_sns_sender import MessageHeaders


fake = Faker()


@pytest.fixture()
def setup_message_headers():
    return MessageHeaders()


def test_get_headers(setup_message_headers):
    assert isinstance(setup_message_headers.get_headers(), dict)


def test_update_headers(setup_message_headers):
    assert setup_message_headers.update_headers(headers={}) is None
