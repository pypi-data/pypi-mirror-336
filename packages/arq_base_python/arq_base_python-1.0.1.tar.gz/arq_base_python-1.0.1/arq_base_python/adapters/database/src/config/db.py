from sqlmodel import create_engine

from arq_base_python.adapters.settings import yaml_settings as settings

engine = create_engine(
    settings.postgres_dsn) if settings.repository.enabled else None
