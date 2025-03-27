import pytest
import random
from faker import Faker

from arq_base_python.cqrs.core.src.jms.message_properties import (
    MessageProperties,
)

fake = Faker()


@pytest.fixture()
def setup_message_properties():
    return MessageProperties()


def test_create_properties(setup_message_properties):
    key = fake.domain_name()
    value = str(random.randint(1, 100))
    setup_message_properties.add(property=key, value=value)
    assert setup_message_properties.get_properties() == {key: value}


def test_add_property(setup_message_properties):
    key = fake.domain_name()
    value = str(random.randint(1, 100))
    setup_message_properties.add(property=key, value=value)
    assert key in setup_message_properties.get_properties()
    assert setup_message_properties.get_properties()[key] == value


def test_add_if_property(setup_message_properties):
    key = fake.domain_name()
    value = str(random.randint(1, 100))
    setup_message_properties.add_if(True, key, lambda: value)
    assert key in setup_message_properties.get_properties()
    assert setup_message_properties.get_properties()[key] == value


def test_add_if_property_false(setup_message_properties):
    key = fake.domain_name()
    value = str(random.randint(1, 100))
    setup_message_properties.add_if(False, key, lambda: value)
    assert key not in setup_message_properties.get_properties()
