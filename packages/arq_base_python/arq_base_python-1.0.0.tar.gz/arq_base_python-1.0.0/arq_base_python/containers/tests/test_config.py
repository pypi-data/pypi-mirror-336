import pytest
from containers.config import ListenerConfig

from unittest.mock import MagicMock
import pytest


@pytest.mark.asyncio
async def test_config_initialization():
    # Arrange: Crear un diccionario simulado para la configuración del servidor

    # Crear un mock para AwsListenerConfig
    mock_aws_config = MagicMock()
    mock_aws_config.get_listener.return_value = "mock_listener"

    # Act: Crear una instancia de Config
    config = ListenerConfig(
        aws_config=mock_aws_config,
    )

    # Assert: Verificar que los valores inyectados son correctos
    assert config.get_aws_listener() == "mock_listener"
