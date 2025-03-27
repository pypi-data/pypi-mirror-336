import json
from fastapi.responses import JSONResponse
import pytest
from faker import Faker
from unittest.mock import MagicMock, Mock
from fastapi import Request
from reactivex import of

from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_authorizer import CommandAuthorizer
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_body_validator import CommandBodyValidator
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_handler import COMMAND_FIELD, CommandHandler
from arq_base_python.cqrs.core_api.src.models.command_submitted import CommandSubmitted
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_service import CommandService
from arq_base_python.cqrs.core_api.src.models.command import Command


fake = Faker()


@pytest.fixture()
def setup_command_body_validator():
    return MagicMock(spec=CommandBodyValidator)


@pytest.fixture()
def setup_command_command_authorizer():
    return MagicMock(spec=CommandAuthorizer)


@pytest.fixture()
def setup_command_service():
    return MagicMock(spec=CommandService)


@pytest.fixture()
def setup_request():
    return MagicMock(spec=Request)


@pytest.fixture
def setup_command_handler(setup_command_body_validator, setup_command_command_authorizer, setup_command_service):
    return CommandHandler(
        command_body_validator=setup_command_body_validator,
        command_authorizer=setup_command_command_authorizer,
        command_service=setup_command_service
    )


@pytest.fixture()
def setup_command():
    return CommandSubmitted(comando=Command())


def test_setup(setup_command_handler):
    assert setup_command_handler


"""
def test_receive_command(setup_command_handler, setup_request, setup_command):
    breakpoint()
    setup_request.json = setup_command
    breakpoint()
    a = setup_command_handler.receive_command(request=setup_request)
    breakpoint()
    assert setup_command_handler.receive_command(request=setup_request)
"""


def test_get_nombre_comando(setup_command_handler, setup_command):
    assert setup_command_handler._get_nombre_comando(
        command=setup_command) is None


def test_get_nombre_none_comando(setup_command_handler):
    assert setup_command_handler._get_nombre_comando(command=None) == "-vacio-"


@pytest.mark.asyncio
async def test_receive_command_valid(setup_command_handler, setup_request):
    # Arrange
    setup_request.json.return_value = {
        COMMAND_FIELD: {"nombre": "test_command"}}
    mock_command_submitted = MagicMock()
    mock_command_submitted.run.return_value = None
    mock_command_submitted.get_validation_status.return_value = 0
    mock_command_submitted.get.return_value.nombre = "test_command"

    setup_command_handler.command_body_validator.perform_validation.return_value = of(
        mock_command_submitted)
    setup_command_handler.command_authorizer.authorize_recieve_command.return_value = True
    setup_command_handler.command_service.process_command.return_value = JSONResponse(
        content={"status": "success"}, status_code=200)

    # Act
    response = await setup_command_handler.receive_command(
        setup_request, setup_request.json())

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    assert json.loads(response.body) == {"status": "success"}


@pytest.mark.asyncio
async def test_receive_command_invalid(setup_command_handler, setup_request):
    # Arrange
    setup_request.json.return_value = {
        COMMAND_FIELD: {"nombre": "test_command"}}
    mock_command_submitted = MagicMock()
    mock_command_submitted.run.return_value = None
    mock_command_submitted.get_validation_status.return_value = 400
    mock_command_submitted.get_validation_message.return_value = "Invalid command"
    mock_command_submitted.get.return_value.nombre = "test_command"

    setup_command_handler.command_body_validator.perform_validation.return_value = of(
        mock_command_submitted)

    # Act
    response = await setup_command_handler.receive_command(
        setup_request, setup_request.json())

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 400
    assert json.loads(response.body) == {
        "codigo": "400",
        "comando": "test_command",
        "mensaje": "Invalid command"
    }


@pytest.mark.asyncio
async def test_receive_command_no_authorization(setup_command_handler, setup_request):
    # Arrange
    setup_request.json.return_value = {
        COMMAND_FIELD: {"nombre": "test_command"}}
    mock_command_submitted = MagicMock()
    mock_command_submitted.run.return_value = None
    mock_command_submitted.get_validation_status.return_value = 0
    mock_command_submitted.get.return_value.nombre = "test_command"

    setup_command_handler.command_body_validator.perform_validation.return_value = of(
        mock_command_submitted)
    setup_command_handler.command_authorizer.authorize_recieve_command.return_value = False

    # Act
    response = await setup_command_handler.receive_command(
        setup_request, setup_request.json())

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 403
    assert json.loads(response.body) == {
        "codigo": "403",
        "comando": "test_command",
        "mensaje": "No tiene autorizacion para invocar el comando"
    }


@pytest.mark.asyncio
async def test_receive_command_no_command_data(setup_command_handler, setup_request):
    # Arrange
    setup_request.json.return_value = {}
    mock_command_submitted = MagicMock()
    mock_command_submitted.run.return_value = None
    mock_command_submitted.get_validation_status.return_value = 0
    mock_command_submitted.get.return_value.nombre = "test_command"

    setup_command_handler.command_body_validator.perform_validation.return_value = of(
        mock_command_submitted)
    setup_command_handler.command_authorizer.authorize_recieve_command.return_value = True
    setup_command_handler.command_service.process_command.return_value = JSONResponse(
        content={"status": "success"}, status_code=200)

    # Act
    response = await setup_command_handler.receive_command(
        setup_request, setup_request.json())

    # Assert
    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    assert json.loads(response.body) == {"status": "success"}
