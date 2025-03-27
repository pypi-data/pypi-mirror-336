import pytest
from faker import Faker


from arq_base_python.cqrs.core_api.src.properties.mq_destinations import MQDestinations


fake = Faker()


@pytest.fixture()
def get_data():
    return {
        "publish_destination": fake.domain_name(),
        "error_destination": "",
        "subscribe_destination": fake.domain_name(),
        "ui_destination": fake.domain_name()
    }


@pytest.fixture()
def setup_destinations(get_data):
    return MQDestinations(
        publish_destination=get_data.get("publish_destination"),
        suscribre_destination=get_data.get("subscribe_destination"),
        ui_destination=get_data.get("ui_destination")
    )


def test_mq_destinations(get_data, setup_destinations):
    assert (setup_destinations.get_publish_destination()
            == get_data.get("publish_destination"))
    assert (setup_destinations.get_suscribre_destination()
            == get_data.get("subscribe_destination"))
    assert (setup_destinations.get_ui_destination()
            == get_data.get("ui_destination"))
