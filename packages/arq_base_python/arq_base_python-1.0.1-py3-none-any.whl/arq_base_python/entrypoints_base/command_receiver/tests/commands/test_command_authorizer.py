import pytest
from faker import Faker

from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_authorizer import CommandAuthorizer

fake = Faker()


@pytest.fixture()
def setup_command_authorizer():
    command_authorizer = CommandAuthorizer()
    return command_authorizer


def test_command_authorizer(setup_command_authorizer):
    assert setup_command_authorizer
