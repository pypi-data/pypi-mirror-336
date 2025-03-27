from pathlib import Path
from typing import Self, Optional
from boto3 import Session
from pydantic import PostgresDsn, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource
from adapters.aws.src.config.boto3_session_factory import Boto3SessionFactory
from adapters.database.src.config.db_settings import DatabaseConnectionFactory


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: Optional[str] = None
    name: str
    schema_name: str

    @field_validator('host')
    def validate_host(cls, v):
        if not v:
            raise ValueError('Host de base de datos no puede ser vacío')
        return v

    @field_validator('port')
    def validate_port(cls, v):
        if v <= 0 or v > 65535:
            raise ValueError('El puerto debe ser un número entre 1 y 65535')
        return v


class RepositoryAdapter(BaseSettings):
    database: DatabaseSettings
    enabled: bool = True


class CloudSettings(BaseSettings):
    aws: dict


class MQSettings(BaseSettings):
    developerMode: bool
    model_config = SettingsConfigDict(extra='ignore')


class ServerSettings(BaseSettings):
    mq: MQSettings
    model_config = SettingsConfigDict(extra='ignore')


class Settings(BaseSettings):
    server: Optional[ServerSettings] = Field(validation_alias='server')
    repository: Optional[RepositoryAdapter] = Field(
        validation_alias='repository')
    cloud: Optional[CloudSettings] = Field(validation_alias='cloud')

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        return cls(**YamlConfigSettingsSource(cls, path)())

    class Config:
        extra = 'ignore'
        env_ignore_empty = True

    @property
    def develperMode(self) -> bool:
        return self.server.mq.developerMode

    @property
    def postgres_dsn(self) -> PostgresDsn:
        """Obtiene el DSN para conectar con la base de datos."""
        if not self.repository or not self.repository.enabled:
            # Retorna una cadena vacía si no está habilitado
            return ''
        connection_factory = DatabaseConnectionFactory(
            host=self.repository.database.host,
            port=self.repository.database.port,
            user=self.repository.database.user,
            password=self.repository.database.password,
            database=self.repository.database.name,
            schema=self.repository.database.schema_name,
            session=self.get_session
        )
        return connection_factory.get_connection_string(self.develperMode)

    @property
    def get_url(self) -> str:
        """Retorna la URL del DSN como cadena."""
        return str(self.postgres_dsn)

    @property
    def get_session(self) -> Session:
        """Obtiene la sesión de boto3."""
        return Boto3SessionFactory(self.get_data).get_session()

    @property
    def get_data(self) -> dict:
        """Obtiene los datos configurados para AWS."""
        return {'cloud': self.cloud.model_dump()}


yaml_settings = Settings.from_yaml(Path('application.yml'))  # type: ignore
