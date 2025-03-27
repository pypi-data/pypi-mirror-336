import pytest
from adapters.database.src.db_connection import init, main
from unittest.mock import MagicMock, patch

from sqlmodel import select


@pytest.fixture
def mock_engine():
    return MagicMock()


def test_init_successful_connection(mock_engine) -> None:

    try:
        init(mock_engine)
        connection_successful = True
    except Exception:
        connection_successful = False

    assert (
        connection_successful
    )

    assert mock_engine.exec.called_once_with(
        select(1)
    )


@patch('adapters.database.src.db_connection.logger')
def test_main(mock_logger, mock_engine):
    with patch('adapters.database.src.db_connection.init') as mock_init:
        main(mock_engine)
        mock_logger.info.assert_any_call(
            "Iniciando adaptador de base de datos")
        mock_logger.info.assert_any_call(
            "Adaptador de base de datos inicializado")
        mock_init.assert_called_once()
