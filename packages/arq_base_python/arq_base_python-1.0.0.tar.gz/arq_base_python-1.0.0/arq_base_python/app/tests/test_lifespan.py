import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import FastAPI
from adapters.aws.src.config.boto3_session_factory import Boto3SessionFactory
import app.lifespan as lf


@pytest.fixture
def mock_settings():
    """
    Fixture para crear un mock de boto3.session.Session.
    """
    # mock_settings = Ma
    with patch("app.lifespan.yaml_settings") as mock_settings:
        yield mock_settings


@pytest.fixture
def mock_boto3_session():
    """
    Fixture para crear un mock de boto3.session.Session.
    """
    with patch("app.lifespan.Session") as mock_boto3_session:
        yield mock_boto3_session


@patch("app.lifespan.psycopg.connect")
def test_test_db_connection_with_iam_token(mock_connect, mock_settings):
    """
    Test para la función test_db_connection_with_iam_token.
    """
    # Configurar los mocks para evitar conexiones reales
    mock_client = MagicMock()
    mock_settings.get_session.client.return_value = mock_client
    mock_client.generate_db_auth_token.return_value = "mocked_token"

    # Llamar a la función que estamos probando
    lf.test_db_connection_with_iam_token()

    # Verificar que el token de autenticación fue generado
    mock_client.generate_db_auth_token.assert_called_once()
    # Verificar que se intentó conectar a la base de datos
    mock_connect.assert_called_once()
    # Verificar que el token fue usado en la conexión
    assert "password=mocked_token" in mock_connect.call_args[1]["conninfo"]


@patch("app.lifespan.ListenerConfig")
def test_active_listener(mock_config):
    """
    Test para la función active_listener.
    """
    # Configurar el mock para el listener de SQS
    mock_config_instance = mock_config.return_value
    mock_aws_listener = MagicMock()
    mock_config_instance.get_aws_listener.return_value = mock_aws_listener

    # Llamar a la función que estamos probando
    lf.active_listener()

    # Verificar que se inició el hilo y se ejecutó el listener
    mock_aws_listener.start_thread.assert_called_once()
    mock_aws_listener.run_listener.assert_called_once()


@patch("app.lifespan.subprocess.run")
async def test_run_alembic_migrations(mock_subprocess_run):
    """
    Test para la función run_alembic_migrations.
    """
    # Llamar a la función que estamos probando
    await lf.run_alembic_migrations()

    # Verificar que se ejecutó el comando de Alembic
    mock_subprocess_run.assert_called_once_with(
        ["alembic", "upgrade", "head"], check=True)


@pytest.fixture
def app():
    return FastAPI()


@pytest.mark.asyncio
async def test_lifespan(app):
    with patch('app.lifespan.active_listener') as mock_active_listener, \
            patch('app.lifespan.S3Init') as mock_s3_init, \
            patch('app.lifespan.test_db_connection_with_iam_token') as mock_test_db_connection, \
            patch('app.lifespan.db_connection') as mock_db_connection, \
            patch('app.lifespan.run_alembic_migrations', new_callable=AsyncMock) as mock_run_alembic_migrations, \
            patch('app.lifespan.engine', new_callable=AsyncMock) as mock_engine:

        mock_engine.return_value = True

        async with lf.lifespan(app):
            # mock_s3_init.assert_called_once()
            mock_active_listener.assert_called_once()
            mock_test_db_connection.assert_not_called()
            mock_db_connection.assert_called_once_with(mock_engine)
            mock_run_alembic_migrations.assert_awaited_once()
