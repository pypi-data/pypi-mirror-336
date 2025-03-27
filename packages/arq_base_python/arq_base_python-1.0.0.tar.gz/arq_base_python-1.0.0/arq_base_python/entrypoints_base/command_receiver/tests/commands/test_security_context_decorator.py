import pytest
import random
import uuid
from types import SimpleNamespace
from faker import Faker
from reactivex import of

from fastapi.requests import Request
from unittest.mock import MagicMock, patch


from cqrs.core_api.src.models.command_submitted import CommandSubmitted
from cqrs.core_api.src.models.dni import Dni
from cqrs.core_api.src.models.usuario import Usuario
from jano.core.src.request_metadata import RequestMetadata
from cqrs.core_api.src.models.command import Command
from entrypoints_base.command_receiver.src.commands.web.rest_security_context_decorator import RestSecurityContextDecorator
from entrypoints_base.command_receiver.tests import support_data
from jano.core.src.identity.identificacion import Identificacion
from jano.core.src.realm import Realm
from jano.core.src.secured_application import SecuredApplication
from jano.core.src.user_properties import UserProperties


fake = Faker()


@pytest.fixture()
def get_user_properties():
    user_properties = UserProperties()
    user_properties.identificacion = Identificacion(
        tipoId=support_data.default_identification_type, id=support_data.default_channel
    )
    user_properties.subject = "anonymous"
    user_properties.ipAddress = fake.ipv4_private()
    user_properties.uuidSession = str(uuid.uuid4())
    user_properties.realm = Realm.EMPLEADOS
    return user_properties


@pytest.fixture()
def get_request(get_user_properties):
    request = SimpleNamespace(**{
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        "client": {
            "host": fake.ipv4_private()
        },
        "userProperties": get_user_properties
    })
    return request


@pytest.fixture()
def get_request_mock():
    request_mock = MagicMock(spec=Request)
    request_mock.headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    request_mock.client.host = fake.ipv4_private()
    return request_mock


@pytest.fixture()
def get_request_metadata(get_user_properties):
    request_metadata = RequestMetadata()
    request_metadata.userProperties = get_user_properties
    return request_metadata


@pytest.fixture()
def get_command():
    command = Command()
    command.payload = fake.text(5)
    command.nombre = fake.name()
    return command


@pytest.fixture()
def get_cmd_container(get_command):
    command_submitted = CommandSubmitted(comando=get_command)
    return command_submitted


@pytest.fixture()
def get_secured_application():
    secured_application = SecuredApplication()
    secured_application.id_app_proteccion = 100
    secured_application.name = "acmeApp"
    secured_application.jano_enabled = False
    return secured_application


@pytest.fixture()
def start_security_context_decorator(get_secured_application):
    rest_security_context_decorator = RestSecurityContextDecorator(
        secured_application=get_secured_application)
    return rest_security_context_decorator


@pytest.fixture()
def get_short_command():
    return {
        "comando": {
            "nombre": support_data.default_command_name,
            "version": str(float(random.randint(1, 3))),
            "payload": {
                "name": fake.name(),
                "isDone": False,
                "description": fake.text(10),
                "tags": [
                    {
                        "name": fake.name()
                    },
                    {
                        "name": fake.name()
                    }
                ]
            },
            "usuario": {
                "nombre": fake.name(),
                "canal": support_data.default_channel
            },
            "dni": {
                "tipoIdentificacion": support_data.default_identification_type
            }
        }
    }


@pytest.fixture()
def get_short_command_submitted(get_short_command):
    return of(CommandSubmitted(comando=Command(**get_short_command.get("comando"))))


# def test_should_enrich_properties(get_cmd_container, get_request_mock, start_security_context_decorator):
#     assert (start_security_context_decorator.enrich_with_security_props(
#         command=get_cmd_container, context=get_request_mock))


def test_receive_command_submitted_timestamp_validator(get_short_command_submitted, start_security_context_decorator):
    assert (start_security_context_decorator.receive_command_submitted_timestamp_validator(
        observer_object=get_short_command_submitted
    ))


@pytest.fixture()
def get_command_submitted_timestamp(get_short_command_submitted, start_security_context_decorator):
    return start_security_context_decorator.receive_command_submitted_timestamp_validator(
        observer_object=get_short_command_submitted
    )


def test_receive_command_submitted_issuer_app_validator(get_command_submitted_timestamp, start_security_context_decorator):
    assert (start_security_context_decorator.receive_command_submitted_issuer_app_validator(
        observer_object=of(get_command_submitted_timestamp)
    ))


def test___getPrincipal(start_security_context_decorator):
    # Arrange
    decorator = start_security_context_decorator
    decorator.host = "127.0.0.1:8000"
    decorator.headers = {
        "canal": "test_canal",
        "Authorization": "Bearer test_token"
    }

    # Act
    result = decorator._RestSecurityContextDecorator__getPrincipal()

    # Assert
    assert isinstance(result, RequestMetadata)
    assert isinstance(result.userProperties, UserProperties)
    assert result.userProperties.groups == []
    assert result.userProperties.roles == []
    assert result.userProperties.subject == "anonymous"
    assert result.userProperties.accountEnabled is True
    assert isinstance(result.userProperties.identificacion, Identificacion)
    assert result.userProperties.identificacion.id == "00000"
    assert result.userProperties.identificacion.tipoId == "XX"
    assert result.userProperties.nivelSeguridad == 5
    assert result.userProperties.ipAddress == "127.0.0.1"
    assert result.userProperties.displayName == "Usuario Anonimo Jano No Activado"
    assert result.userProperties.givenName == "Jano No activado"
    assert result.userProperties.surName == "Usuario Anonimo"


def test_enrich_with_security_props(get_cmd_container, get_request_mock, start_security_context_decorator, get_request_metadata):
    # Arrange
    command = get_cmd_container
    context = get_request_mock
    decorator = start_security_context_decorator
    request_metadata = get_request_metadata

    # Act
    result = decorator.enrich_with_security_props(
        command, context)

    # Assert
    assert isinstance(result, CommandSubmitted)
    assert result.get() == command.get()
    assert result.get().payload == command.get().payload
    assert result.get().nombre == command.get().nombre
    assert result.get().usuario.nombre == request_metadata.userProperties.subject
    assert result.get().usuario.canal == support_data.default_channel
    # assert result.get().dni.tipo_identificacion == support_data.default_identification_type
    # assert result.get().dni.identificacion == context.userProperties.identificacion.id


@pytest.fixture
def secured_application():
    return SecuredApplication()


@pytest.fixture
def rest_security_context_decorator(secured_application):
    return RestSecurityContextDecorator(secured_application)


@pytest.fixture
def command_submitted():
    command = MagicMock(spec=CommandSubmitted)
    command.get.return_value.usuario = None
    return command


@pytest.fixture
def user_properties():
    user_properties = UserProperties()
    user_properties.realm = Realm.EMPLEADOS
    user_properties.uuidSession = str(uuid.uuid4())
    return user_properties


def test_process_user_data_no_usuario(rest_security_context_decorator, command_submitted):
    # Act
    result = rest_security_context_decorator._RestSecurityContextDecorator__process_user_data(
        command_submitted)

    # Assert
    assert isinstance(result, CommandSubmitted)
    assert result.get().usuario is not None
    assert result.get().usuario.dni == "DNI_NO_DISPONIBLE"
    assert result.get().usuario.nombre == "USUARIO_NO_DISPONIBLE"
    assert result.get().usuario.id_session == "SESION_NO_DISPONIBLE"
    assert result.get().usuario.canal == "CANAL_NO_INDICADO"
    assert result.get().usuario.telefono == "TELEFONO_NO_INDICADO"


def test_process_user_data_with_usuario(rest_security_context_decorator):
    # Arrange
    usuario = Usuario()
    usuario.dni = "12345678"
    usuario.nombre = "Test User"
    usuario.id_session = "session123"
    usuario.canal = "Test Canal"
    usuario.telefono = "1234567890"

    command_submitted = MagicMock(spec=CommandSubmitted)
    command_submitted.get.return_value.usuario = usuario

    # Act
    result = rest_security_context_decorator._RestSecurityContextDecorator__process_user_data(
        command_submitted)

    # Assert
    assert isinstance(result, CommandSubmitted)
    assert result.get().usuario is not None
    assert result.get().usuario.dni == "12345678"
    assert result.get().usuario.nombre == "Test User"
    assert result.get().usuario.id_session == "session123"
    assert result.get().usuario.canal == "Test Canal"
    assert result.get().usuario.telefono == "1234567890"


def test_parseUuidSession_no_realm(rest_security_context_decorator, command_submitted, user_properties):
    # Arrange
    usuario = Usuario()
    user_properties.realm = None
    command_submitted.get.return_value.usuario = usuario

    # Act
    result = rest_security_context_decorator._RestSecurityContextDecorator__parseUuidSession(
        command_submitted, user_properties)

    # Assert
    assert isinstance(result, CommandSubmitted)
    assert result.get().usuario.id_session == "SESION_NO_DISPONIBLE"


def test_parseUuidSession_with_realm_no_uuidSession(rest_security_context_decorator, command_submitted, user_properties):
    # Arrange
    usuario = Usuario()
    user_properties.uuidSession = None
    command_submitted.get.return_value.usuario = usuario

    # Act
    result = rest_security_context_decorator._RestSecurityContextDecorator__parseUuidSession(
        command_submitted, user_properties)

    # Assert
    assert isinstance(result, CommandSubmitted)
    assert result.get().usuario.id_session == "SESION_NO_DISPONIBLE"


def test_process_header_valid(rest_security_context_decorator):
    # Arrange
    header_value = "CC12345"

    # Act
    result = rest_security_context_decorator._RestSecurityContextDecorator__process_header(
        header_value)

    # Assert
    assert isinstance(result, Dni)
    assert result.identificacion == "12345"
    assert result.tipo_identificacion == "CC"


def test_process_header_invalid(rest_security_context_decorator):
    # Arrange
    header_value = "InvalidHeader"

    # Act
    result = rest_security_context_decorator._RestSecurityContextDecorator__process_header(
        header_value)

    # Assert
    assert isinstance(result, Dni)
    assert result.identificacion == None
    assert result.tipo_identificacion == None
