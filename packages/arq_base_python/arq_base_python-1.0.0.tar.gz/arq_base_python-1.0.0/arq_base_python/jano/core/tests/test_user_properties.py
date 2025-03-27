import pytest
from jano.core.src.user_properties import UserProperties
from jano.core.src.identity.identificacion import Identificacion


@pytest.fixture
def user_properties():
    return UserProperties()


def test_user_properties(user_properties):
    # Arrange: Inicialización del objeto user_properties
    user = user_properties

    # Act: No hay acciones en esta parte ya que estamos probando la inicialización

    # Assert: Verificar los valores iniciales
    assert user.subject == None
    assert user.displayName == None
    assert user.givenName == None
    assert user.surName == None
    assert user.email == None
    assert user.identificacion == Identificacion()
    assert user.roles == []
    assert user.groups == []
    assert user.nivelSeguridad == 5
    assert user.realm == None
    assert user.userType == None
    assert user.ipAddress == None
    assert user.uuidSession == None
    assert user.accountEnabled == False
    assert user.objectId == None

    # Arrange: Preparar nuevos valores para las propiedades
    new_values = {
        "subject": "JohnDoe",
        "displayName": "John Doe",
        "givenName": "John",
        "surName": "Doe",
        "email": "john.doe@example.com",
        "identificacion": {"type": "ID", "number": "123456789"},
        "roles": ["admin", "user"],
        "groups": ["group1", "group2"],
        "nivelSeguridad": 10,
        "realm": "example",
        "userType": "regular",
        "ipAddress": "127.0.0.1",
        "uuidSession": "1234567890",
        "accountEnabled": True,
        "objectId": "abcdef123456"
    }

    # Act: Asignar nuevos valores a las propiedades
    user.subject = new_values["subject"]
    user.displayName = new_values["displayName"]
    user.givenName = new_values["givenName"]
    user.surName = new_values["surName"]
    user.email = new_values["email"]
    user.identificacion = new_values["identificacion"]
    user.roles = new_values["roles"]
    user.groups = new_values["groups"]
    user.nivelSeguridad = new_values["nivelSeguridad"]
    user.realm = new_values["realm"]
    user.userType = new_values["userType"]
    user.ipAddress = new_values["ipAddress"]
    user.uuidSession = new_values["uuidSession"]
    user.accountEnabled = new_values["accountEnabled"]
    user.objectId = new_values["objectId"]

    # Assert: Verificar que los valores se hayan asignado correctamente
    assert user.subject == new_values["subject"]
    assert user.displayName == new_values["displayName"]
    assert user.givenName == new_values["givenName"]
    assert user.surName == new_values["surName"]
    assert user.email == new_values["email"]
    assert user.identificacion == new_values["identificacion"]
    assert user.roles == new_values["roles"]
    assert user.groups == new_values["groups"]
    assert user.nivelSeguridad == new_values["nivelSeguridad"]
    assert user.realm == new_values["realm"]
    assert user.userType == new_values["userType"]
    assert user.ipAddress == new_values["ipAddress"]
    assert user.uuidSession == new_values["uuidSession"]
    assert user.accountEnabled == new_values["accountEnabled"]
    assert user.objectId == new_values["objectId"]
