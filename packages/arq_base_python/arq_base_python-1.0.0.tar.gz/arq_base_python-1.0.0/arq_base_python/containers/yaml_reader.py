import logging
from pydantic import Field
from pydantic_settings import BaseSettings, YamlConfigSettingsSource
from typing import Optional, Dict, Any, Self
from pathlib import Path
import yaml


class YAMLReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self._log = logging.getLogger(__name__)

    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            self._log.error(f"El archivo {self.file_path} no fue encontrado.")
            raise FileNotFoundError(
                f"El archivo {self.file_path} no fue encontrado.")
        except yaml.YAMLError as exc:
            self._log.error(f"Error al leer el archivo YAML: {exc}")
            raise yaml.YAMLError(f"Error al leer el archivo YAML: {exc}")
        else:
            return data


class MQSettings(BaseSettings):
    publishDestination: str
    subscribeDestination: str
    errorDestination: str
    concurrency: str
    aws: Dict[str, Any]
    developerMode: bool


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str
    schema_name: str


class RepositorySettings(BaseSettings):
    database: DatabaseSettings


class StackSettings(BaseSettings):
    auto: bool


class RegionSettings(BaseSettings):
    static: str


class CredentialsSettings(BaseSettings):
    instanceProfile: bool
    use_default_aws_credentials_chain: bool = Field(
        validation_alias='use-default-aws-credentials-chain')
    accessKey: Optional[str]
    secretKey: Optional[str]


class AWSSettings(BaseSettings):
    stack: StackSettings
    region: RegionSettings
    credentials: CredentialsSettings


class CloudSettings(BaseSettings):
    aws: AWSSettings


class ServerSettings(BaseSettings):
    host: str
    port: int
    mq: MQSettings


class YamlData(BaseSettings):
    server: ServerSettings
    repository: RepositorySettings
    cloud: CloudSettings

    @classmethod
    def from_yaml(cls, path: Path) -> Self:
        return cls(**YamlConfigSettingsSource(cls, path)())

    class Config:
        extra = 'ignore'
        env_ignore_empty = True
