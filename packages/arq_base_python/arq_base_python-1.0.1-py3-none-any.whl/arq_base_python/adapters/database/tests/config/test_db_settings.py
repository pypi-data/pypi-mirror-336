import pytest
from unittest.mock import Mock, patch
from boto3 import Session
from arq_base_python.adapters.database.src.config.db_settings import DatabaseConnectionFactory, DatabaseTokenGenerationError


@pytest.fixture
def mock_session():
    return Mock(spec=Session)


@pytest.fixture
def db_factory(mock_session):
    return DatabaseConnectionFactory(
        host="localhost",
        port=5432,
        user="test_user",
        password="test_password",
        database="test_db",
        schema="public",
        session=mock_session
    )


URI_PASSWORD_EXPECTED = "postgresql+psycopg://test_user:test_password@localhost:5432/test_db?options=-c%20search_path=public"
URI_IAM_EXPECTED = "postgresql+psycopg://test_user:encoded_token@localhost:5432/test_db?options=-c%20search_path=public"
PATH_TO_MOCK = 'adapters.database.src.config.db_settings'


def test_get_password_connection_string(db_factory):
    connection_string = db_factory.get_password_connection_string()
    assert URI_PASSWORD_EXPECTED in connection_string


def test_get_iam_connection_string(db_factory, mock_session):
    db_factory.password = None
    mock_session.client.return_value.generate_db_auth_token.return_value = "test_token"

    with patch(f"{PATH_TO_MOCK}.quote", return_value="encoded_token"):
        connection_string = db_factory.get_iam_connection_string()
        assert URI_IAM_EXPECTED in connection_string


def test_generate_rds_iam_token(db_factory, mock_session):
    mock_session.client.return_value.generate_db_auth_token.return_value = "test_token"
    token = db_factory.generate_rds_iam_token()
    assert token == "test_token"


def test_generate_rds_iam_token_error(db_factory, mock_session):
    mock_session.client.return_value.generate_db_auth_token.side_effect = Exception(
        "IAM token error")
    with pytest.raises(DatabaseTokenGenerationError, match="Error al generar el token IAM: IAM token error"):
        db_factory.generate_rds_iam_token()


def test_get_connection_string_with_password(db_factory):
    connection_string = db_factory.get_connection_string()
    assert URI_PASSWORD_EXPECTED in connection_string


def test_get_connection_string_with_iam(db_factory, mock_session):
    db_factory.password = None
    mock_session.client.return_value.generate_db_auth_token.return_value = "test_token"

    with patch(f"{PATH_TO_MOCK}.quote", return_value="encoded_token"):
        connection_string = db_factory.get_connection_string(False)
        assert URI_IAM_EXPECTED in connection_string
    with pytest.raises(DatabaseTokenGenerationError, match="Error al generar el token IAM: IAM token error"):
        db_factory.generate_rds_iam_token()


def test_get_connection_string_with_password(db_factory):
    connection_string = db_factory.get_connection_string()
    assert URI_PASSWORD_EXPECTED in connection_string


def test_get_connection_string_with_iam(db_factory, mock_session):
    db_factory.password = None
    mock_session.client.return_value.generate_db_auth_token.return_value = "test_token"

    with patch(f"{PATH_TO_MOCK}.quote", return_value="encoded_token"):
        connection_string = db_factory.get_connection_string(False)
        assert URI_IAM_EXPECTED in connection_string
