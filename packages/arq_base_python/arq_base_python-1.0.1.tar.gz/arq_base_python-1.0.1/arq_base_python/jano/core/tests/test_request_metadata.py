import pytest
from arq_base_python.jano.core.src.request_metadata import RequestMetadata
from arq_base_python.jano.core.src.user_properties import UserProperties


@pytest.fixture
def request_metadata():
    return RequestMetadata(
        restrictions=["restriction1", "restriction2"],
        commandId="command123",
        whitelisted=True,
        userProperties={"subject": "value", "displayName": "value"},
        encabezados=["header1", "header2"],
        ip="192.168.1.1",
        url="http://example.com",
        method="GET",
        parameters=["param1", "param2"]
    )


def test_initialization(request_metadata):
    assert request_metadata.restrictions == ["restriction1", "restriction2"]
    assert request_metadata.commandId == "command123"
    assert request_metadata.whitelisted is True
    assert isinstance(request_metadata.userProperties, UserProperties)
    assert request_metadata.userProperties.subject == "value"
    assert request_metadata.encabezados == ["header1", "header2"]
    assert request_metadata.ip == "192.168.1.1"
    assert request_metadata.url == "http://example.com"
    assert request_metadata.method == "GET"
    assert request_metadata.parameters == ["param1", "param2"]


def test_set_restrictions(request_metadata):
    request_metadata.restrictions = ["new_restriction"]
    assert request_metadata.restrictions == ["new_restriction"]


def test_set_commandId(request_metadata):
    request_metadata.commandId = "new_command"
    assert request_metadata.commandId == "new_command"


def test_set_whitelisted(request_metadata):
    request_metadata.whitelisted = False
    assert request_metadata.whitelisted is False


def test_set_userProperties(request_metadata):
    new_user_properties = UserProperties(subject="new_value")
    request_metadata.userProperties = new_user_properties
    assert request_metadata.userProperties.subject == "new_value"


def test_set_encabezados(request_metadata):
    request_metadata.encabezados = ["new_header"]
    assert request_metadata.encabezados == ["new_header"]


def test_set_ip(request_metadata):
    request_metadata.ip = "10.0.0.1"
    assert request_metadata.ip == "10.0.0.1"


def test_set_url(request_metadata):
    request_metadata.url = "http://newexample.com"
    assert request_metadata.url == "http://newexample.com"


def test_set_method(request_metadata):
    request_metadata.method = "POST"
    assert request_metadata.method == "POST"


def test_set_parameters(request_metadata):
    request_metadata.parameters = ["new_param"]
    assert request_metadata.parameters == ["new_param"]


def test_default_initialization():
    request_metadata = RequestMetadata()
    assert request_metadata.restrictions == []
    assert request_metadata.commandId == None
    assert request_metadata.whitelisted is False
    assert isinstance(request_metadata.userProperties, UserProperties)
    assert request_metadata.encabezados == []
    assert request_metadata.ip == None
    assert request_metadata.url == None
    assert request_metadata.method == None
    assert request_metadata.parameters == []
