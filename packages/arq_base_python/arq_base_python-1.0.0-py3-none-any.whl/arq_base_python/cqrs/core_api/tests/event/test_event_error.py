from datetime import date
import json
import uuid
import random

import pytest
from faker import Faker

from cqrs.core_api.src.event.event_error import EventError
from cqrs.core_api.tests.data_support import DataSupport


fake = Faker()


@pytest.fixture()
def setup_event_error():
    event_error = EventError()
    return event_error


def test_id(setup_event_error):
    value = float(random.randint(1, 10))
    setup_event_error.id = value
    assert isinstance(setup_event_error.id, float)
    assert setup_event_error.id == value


def test_name(setup_event_error):
    value = fake.name()
    setup_event_error.name = value
    assert isinstance(setup_event_error.name, str)
    assert setup_event_error.name == value


def test_uuid(setup_event_error):
    value = str(uuid.uuid4())
    setup_event_error.uuid = value
    assert isinstance(setup_event_error.uuid, str)
    assert setup_event_error.uuid == value


def test_json(setup_event_error):
    value = json.dumps({fake.name(): fake.name()})
    setup_event_error.json = value
    assert isinstance(setup_event_error.json, str)
    assert setup_event_error.json == value


def test_clase(setup_event_error):
    value = fake.name()
    setup_event_error.clase = value
    assert isinstance(setup_event_error.clase, str)
    assert setup_event_error.clase == value


def test_tipo_dni(setup_event_error):
    value = random.choice(DataSupport.identification_types)
    setup_event_error.tipoDni = value
    assert isinstance(setup_event_error.tipoDni, str)
    assert setup_event_error.tipoDni == value


def test_date(setup_event_error):
    value = date.today()
    setup_event_error.fechaEvento = value
    assert isinstance(setup_event_error.fechaEvento, date)
    assert setup_event_error.fechaEvento == value


def test_error_description(setup_event_error):
    value = fake.text(5)
    setup_event_error.errorDescription = value
    assert isinstance(setup_event_error.errorDescription, str)
    assert setup_event_error.errorDescription == value
