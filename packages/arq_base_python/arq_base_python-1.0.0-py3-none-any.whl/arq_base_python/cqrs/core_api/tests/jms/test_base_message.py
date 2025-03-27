import time
import uuid
import random

import pytest
from faker import Faker

from cqrs.core_api.src.jms.base_message import BaseMessage
from cqrs.core_api.tests.data_support import DataSupport

fake = Faker()


@pytest.fixture()
def get_command_id() -> str:
    return str(uuid.uuid4())


@pytest.fixture()
def get_body(get_command_id):
    return {
        "comando": {
            "id": get_command_id,
            "idTrazabilidad": None,
            "nombre": random.choice(DataSupport.command_names),
            "version": None,
            "aplicacionEmisora": {
                "idAplicacionEmisora": random.randint(1, 500),
                "nombreAplicacionEmisora": fake.user_name(),
                "idTransaccionEmisora": None,
                "fechaTransaccion": None
            },
            "aplicacionOrigen": {
                "idAplicacionOrigen": random.randint(1, 500),
                "nombreAplicacionOrigen": fake.user_name()
            },
            "usuario": {
                "dni": "XX-00000",
                "ip": fake.ipv4_private(),
                "nombre": fake.user_name(),
                "canal": DataSupport.not_indicated_channel_message,
                "telefono": fake.phone_number(),
                "idSession": fake.unique.random_int(min=111111, max=999999)
            },
            "dni": {
                "tipoIdentificacion": random.choice(DataSupport.identification_types),
                "identificacion": fake.unique.random_int(min=111111, max=999999)
            },
            "timestamp": time.time(),
            "payload": {
                "name": DataSupport.default_task_name,
                "isDone": False,
                "description": DataSupport.default_description,
                "tags": DataSupport.default_tags
            }
        },
        "validation_status": 0,
        "validation_message": None
    }


@pytest.fixture()
def get_headers():
    return {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "en.wikipedia.org:8080"
    }


@pytest.fixture()
def get_message_id():
    return str(uuid.uuid4())


@pytest.fixture()
def initialize_base_message(get_body, get_headers, get_message_id):
    base_message_object = BaseMessage(
        messageId=get_message_id, headers=get_headers, body=get_body)
    return base_message_object


def test_get_body(initialize_base_message):
    assert initialize_base_message.get_body()


def test_get_headers(initialize_base_message):
    assert initialize_base_message.get_headers()


def test_get_message_id(initialize_base_message):
    assert initialize_base_message.get_message_id()
