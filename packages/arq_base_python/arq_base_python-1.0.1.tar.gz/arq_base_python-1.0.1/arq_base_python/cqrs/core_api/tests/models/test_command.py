import random

import pytest
from faker import Faker


from arq_base_python.cqrs.core_api.src.models.command import Command

fake = Faker()


@pytest.fixture()
def setup_command():
    command = Command()
    return command


def test_command_get_id(setup_command):
    command_id = str(random.randint(1, 10))
    setup_command.id = command_id
    assert (setup_command.id == command_id)


def test_get_payload(setup_command):
    setup_command.payload = "Str"
    assert (setup_command.payload == "Str")
