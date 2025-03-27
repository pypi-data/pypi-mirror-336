from sqlmodel import create_engine

from adapters.settings import yaml_settings as settings

engine = create_engine(
    settings.postgres_dsn) if settings.repository.enabled else None
