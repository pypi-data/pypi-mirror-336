from fastapi.responses import JSONResponse
from unittest.mock import AsyncMock, Mock
import pytest
from unittest.mock import Mock
from reactivex import of

from arq_base_python.cqrs.core_api.src.command.security_helper import SecurityHelper
from arq_base_python.cqrs.core_api.src.messaging.reactive_message_publisher import ReactiveMessagePublisher
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_service import CommandService
from arq_base_python.jano.core.src.secured_application import SecuredApplication
from arq_base_python.cqrs.core_api.src.models.command import Command
from arq_base_python.cqrs.core_api.src.models.command_submitted import CommandSubmitted


@pytest.fixture
def mock_security_helper():
    return Mock(spec=SecurityHelper)


@pytest.fixture
def mock_command_service():
    message_publisher = Mock(spec=ReactiveMessagePublisher)
    secured_application = Mock(spec=SecuredApplication)
    security_helper = Mock(spec=SecurityHelper)

    service = CommandService(
        message_publisher, secured_application, security_helper)
    return service


@pytest.mark.asyncio
async def test_process_command(mock_command_service):
    # Arrange
    command = Mock(spec=CommandSubmitted)
    request = Mock()

    mock_command_service.security_helper.enrich_with_security_props.return_value = command
    mock_command_service._publish = AsyncMock(return_value=True)
    mock_command_service.receive_build_response = Mock(return_value=JSONResponse(
        content={"test": "response"}, status_code=202))

    # Act
    response = await mock_command_service.process_command(command, request)

    # Assert
    # Verifica que el comando fue enriquecido y se ejecutaron los métodos internos
    mock_command_service.security_helper.enrich_with_security_props.assert_called_once_with(
        command, request)
    mock_command_service._publish.assert_called_once()
    mock_command_service.receive_build_response.assert_called_once()

    # Verifica el tipo de respuesta
    assert isinstance(response, JSONResponse)
    assert response.status_code == 202


def test_receive_build_response(mock_command_service):
    # Arrange
    command = Mock(spec=CommandSubmitted)

    # Simula el retorno de _build_response
    mock_command_service._build_response = Mock(return_value=JSONResponse(
        content={"ack": "ok"}, status_code=202))

    observer = of(command)

    # Act
    response = mock_command_service.receive_build_response(observer)

    # Assert
    # Verifica que _build_response fue llamado con el comando correcto
    mock_command_service._build_response.assert_called_once_with(command)

    # Verifica que la respuesta sea la esperada
    assert isinstance(response, JSONResponse)
    assert response.status_code == 202


@pytest.mark.asyncio
async def test_receive_command_sub_enrich(mock_command_service):
    # Arrange
    command = Mock(spec=CommandSubmitted)

    # Simula el retorno de _publish
    mock_command_service._publish = AsyncMock(return_value=True)

    observer = of(command)

    # Act
    result = await mock_command_service.receive_command_sub_enrich(observer)

    # Assert
    # Verifica que _publish fue llamado con el comando correcto
    mock_command_service._publish.assert_called_once_with(command)
    assert result is True


@pytest.mark.asyncio
async def test_publish_valid_command(mock_command_service):
    # Arrange
    command = Mock(spec=CommandSubmitted)

    # Simula que el comando tiene un estado de validación correcto (0)
    command.get_validation_status.return_value = 0

    # Act
    result = await mock_command_service._publish(command)

    # Assert
    # Verifica que publish fue llamado cuando la validación es correcta
    mock_command_service.message_publisher.publish.assert_called_once_with(
        command)
    assert result is True


@pytest.mark.asyncio
async def test_publish_invalid_command(mock_command_service):
    # Arrange
    command = Mock(spec=CommandSubmitted)

    # Simula que el comando tiene un estado de validación incorrecto (no es 0)
    command.get_validation_status.return_value = 1

    # Act
    result = await mock_command_service._publish(command)

    # Assert
    # Verifica que publish no fue llamado cuando la validación es incorrecta
    mock_command_service.message_publisher.publish.assert_not_called()
    assert result is False


async def test_build_response_valid_command(mock_command_service):
    # Arrange
    command = CommandSubmitted(Mock(spec=Command))

    mock_command_service._create_ack = Mock(return_value={"ack": "ok"})

    # Act
    response = mock_command_service._build_response(command)

    # Assert
    # Verifica el código de estado de la respuesta
    assert response.status_code == 202


def test_build_response_invalid_command(mock_command_service):
    # Arrange
    command = CommandSubmitted(Mock(spec=Command))

    # Simula que el comando es inválido
    command.get_validation_status = Mock(return_value=1)
    command.get_validation_message = Mock(return_value="Error")

    # Act
    response = mock_command_service._build_response(command)

    # Assert
    # Verifica el código de estado y el contenido de la respuesta
    assert response.status_code == 422
