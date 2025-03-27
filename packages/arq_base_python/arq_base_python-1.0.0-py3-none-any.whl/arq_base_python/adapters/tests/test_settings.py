import pytest
from pathlib import Path
from pydantic import ValidationError
from unittest.mock import patch, MagicMock
from adapters.settings import Settings, DatabaseSettings, RepositoryAdapter, CloudSettings, ServerSettings, MQSettings


def test_database_settings_validation():
    with pytest.raises(ValidationError):
        DatabaseSettings(host='', port=5432, user='user',
                         name='dbname', schema_name='public')

    with pytest.raises(ValidationError):
        DatabaseSettings(host='localhost', port=70000,
                         user='user', name='dbname', schema_name='public')

    valid_settings = DatabaseSettings(
        host='localhost', port=5432, user='user', name='dbname', schema_name='public')
    assert valid_settings.host == 'localhost'
    assert valid_settings.port == 5432


def test_repository_adapter():
    db_settings = DatabaseSettings(
        host='localhost', port=5432, user='user', name='dbname', schema_name='public')
    repo_adapter = RepositoryAdapter(database=db_settings, enabled=True)
    assert repo_adapter.database.host == 'localhost'
    assert repo_adapter.enabled is True


def test_cloud_settings():
    cloud_settings = CloudSettings(aws={'key': 'value'})
    assert cloud_settings.aws['key'] == 'value'


@patch('adapters.settings.DatabaseConnectionFactory')
@patch('adapters.settings.Boto3SessionFactory')
def test_settings(mock_boto3_factory, mock_db_factory):
    mock_db_factory.return_value.get_connection_string.return_value = 'postgresql://user:password@localhost:5432/dbname'
    mock_boto3_factory.return_value.get_session.return_value = MagicMock()

    settings = Settings(
        repository=RepositoryAdapter(
            database=DatabaseSettings(
                host='localhost',
                port=5432,
                user='user',
                password='password',
                name='dbname',
                schema_name='public'
            ),
            enabled=True
        ),
        cloud=CloudSettings(aws={'key': 'value'}),
        server=ServerSettings(
            mq=MQSettings(
                developerMode=True
            )
        )
    )

    assert settings.postgres_dsn == 'postgresql://user:password@localhost:5432/dbname'
    assert settings.get_url == 'postgresql://user:password@localhost:5432/dbname'
    assert isinstance(settings.get_session, MagicMock)
    assert settings.get_data == {'cloud': {'aws': {'key': 'value'}}}


def test_from_yaml():
    with patch('adapters.settings.Path.open', MagicMock(return_value=open('application.yml'))):
        settings = Settings.from_yaml(Path('application.yml'))
        assert isinstance(settings, Settings)
