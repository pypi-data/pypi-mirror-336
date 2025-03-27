import pytest
from unittest import mock
from entrypoints_base.command_receiver.src.commands.web.command_body_validator import (
    CommandBodyValidator,
)
from cqrs.core_api.src.models.command_submitted import (
    CommandSubmitted,
)
from cqrs.core_api.src.models.handler_registry import (
    HandlerRegistry,
)
from entrypoints_base.command_receiver.src.commands.invalid_regex import (
    InvalidRegex,
)
from cqrs.core_api.src.models.command import Command


@pytest.fixture
def setup_command_body_validator():
    handler_registry = HandlerRegistry()
    invalid_regex = InvalidRegex()
    command_body_validator = CommandBodyValidator(
        handler_registry, invalid_regex)
    return command_body_validator


def test_valid_contract(setup_command_body_validator):
    command = CommandSubmitted()
    result = setup_command_body_validator._valid_contract(command)
    assert result.get_validation_status() == 400
    assert result.get_validation_message() == "Nombre del comando es obligatorio"


def test_command_declared_in_handler_registry(setup_command_body_validator):
    command = CommandSubmitted()
    handler_registry = HandlerRegistry()
    handler_registry.command_handlers = ["command1", "command2"]
    result = setup_command_body_validator._validate_command_name(
        command, handler_registry)
    assert result.get_validation_status() == 400
    assert result.get_validation_message() == "Nombre del comando no registrado"


"""
def test_validate_command_special_characters(setup_command_body_validator):
    command = CommandSubmitted()
    result = setup_command_body_validator._validate_command_special_characters(command=command)
    assert result.get_validation_status() == 0
    assert result.get_validation_message() == None
"""


def test_validate_command_name_registered(setup_command_body_validator):
    command_sub = CommandSubmitted(comando=Command(nombre="command1"))
    handler_registry = HandlerRegistry()
    handler_registry.command_handlers = ["command1", "command2"]
    result = setup_command_body_validator._validate_command_name(
        command_sub, handler_registry
    )
    assert result.get_validation_status() == 400
    assert result.get_validation_message() == "Nombre del comando no registrado"


@pytest.fixture
def invalid_regex_mock():
    # Mock para InvalidRegex
    regex_mock = mock.create_autospec(InvalidRegex)
    regex_mock.get_regex.return_value = r"[~!@#&|;\'?/*$^+\\\\<>]"
    return regex_mock


@pytest.fixture
def command_submitted_mock():
    # Mock para CommandSubmitted con un Command que tenga atributos
    command = Command(
        id="123", nombre="ValidCommand", payload={"data": "valid_data"}
    )
    # Simula que la validación está bien al inicio
    return CommandSubmitted(comando=command)


@pytest.fixture
def command_body_validator(invalid_regex_mock):
    # Instancia de CommandBodyValidator con los mocks inyectados
    return CommandBodyValidator(handler_registry=None, invalid_regex=invalid_regex_mock)


def test_validate_command_special_characters_no_special_characters(
    command_body_validator, command_submitted_mock
):
    # Arrange: Preparamos los mocks con datos válidos (sin caracteres especiales)
    command = command_submitted_mock

    # Act: Llamamos al método privado usando name mangling para acceder al método protegido
    result = command_body_validator._validate_command_special_characters(
        command)

    # Assert: Verificamos que el estado de validación y mensaje sean correctos
    assert result.get_validation_status() == 0  # Asegura que no haya errores
    # No debería haber mensaje de error
    assert result.get_validation_message() is None


def test_validate_command_special_characters_with_special_characters(
    command_body_validator, command_submitted_mock
):
    # Arrange: Modificamos el payload para contener caracteres especiales
    command = command_submitted_mock
    command.get().payload = {"data": "invalid_data~"}

    # Act: Llamamos al método privado usando name mangling
    result = command_body_validator._validate_command_special_characters(
        command)

    # Assert: Verificamos que el estado de validación sea de error y el mensaje sea adecuado
    assert result.get_validation_status() == 400  # Código de error esperado
    assert "Contiene caracteres no permitidos" in result.get_validation_message()
