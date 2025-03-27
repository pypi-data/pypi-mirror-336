import pytest
from faker import Faker


from arq_base_python.cqrs.core_api.src.models.command_submitted import CommandSubmitted
from arq_base_python.cqrs.core_api.src.models.command import Command

fake = Faker()


@pytest.fixture()
def setup_command():
    command = Command()
    return command


@pytest.fixture()
def setup_command_submitted(setup_command):
    command_submitted = CommandSubmitted(comando=setup_command)
    return command_submitted


def test_command_constructor(setup_command_submitted, setup_command):
    assert (setup_command_submitted.get() == setup_command)
    assert (setup_command_submitted.get_validation_status() == 0)
    assert (setup_command_submitted.get_validation_message() is None)
