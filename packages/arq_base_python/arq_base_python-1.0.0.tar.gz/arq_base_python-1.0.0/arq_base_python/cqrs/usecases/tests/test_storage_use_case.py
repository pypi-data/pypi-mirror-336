import pytest
from unittest.mock import MagicMock, patch
from reactivex import throw
from reactivex import operators as op

from cqrs.core_api.src.storage.bucket_service import BucketService
from cqrs.core_api.src.storage.file_service import FileService
from cqrs.usecases.src.storage_use_case import StorageUseCase


# Mock de las dependencias
@pytest.fixture
def mock_file_service():
    return MagicMock(spec=FileService)


@pytest.fixture
def mock_bucket_service():
    return MagicMock(spec=BucketService)


@pytest.fixture
def storage_use_case(mock_file_service, mock_bucket_service):
    return StorageUseCase(mock_file_service, mock_bucket_service)


def test_list_by_page_success(storage_use_case, mock_file_service, mock_bucket_service):
    # Arrange
    mock_bucket_service.get_info.return_value.name = "test_bucket"
    mock_file_service.list.return_value.pipe.return_value = MagicMock()

    # Act
    result = storage_use_case.list_by_page(1, 10)

    # Verificar que se llamó a los métodos correctos
    mock_bucket_service.get_info.assert_called_once()
    mock_file_service.list.assert_called_once_with("test_bucket")
    mock_file_service.list.return_value.pipe.assert_called_once()


def test_list_by_page_exception(storage_use_case, mock_file_service, mock_bucket_service):
    # Arrange
    mock_bucket_service.get_info.return_value.name = "test_bucket"
    mock_file_service.list = MagicMock(
        side_effect=Exception("Test error"))
    storage_use_case.log = MagicMock()

    # Act/Assert
    with pytest.raises(Exception):
        result = storage_use_case.list_by_page(1, 10)
        assert isinstance(result, throw)
        storage_use_case.log.error.assert_called_once_with(
            f"Error listando archivos: Test errorx")


def test_list_by_page_handles_error(storage_use_case, mock_file_service, mock_bucket_service):
    # Arrange
    mock_bucket_service.get_info.return_value.name = "test-bucket"
    mock_file_service.list.return_value = throw(Exception("Test error"))
    storage_use_case.log = MagicMock()

    # Act
    result = storage_use_case.list_by_page(1, 10)
    # Convertir el Observable a una lista para forzar la ejecución
    result.subscribe(
        on_next=lambda x: x,
        on_error=lambda e: e
    )

    # Assert
    storage_use_case.log.error.assert_called_with(
        "Error listando archivos: Test error")


def test_list_all(storage_use_case, mock_file_service, mock_bucket_service):
    # Configurar los mocks
    mock_bucket_service.get_info.return_value.name = "test_bucket"
    mock_file_service.list.return_value.pipe.return_value = MagicMock()

    # Llamar al método bajo prueba
    result = storage_use_case.list_all()

    # Verificar que se llamó a los métodos correctos
    mock_bucket_service.get_info.assert_called_once()
    mock_file_service.list.assert_called_once_with("test_bucket")
    mock_file_service.list.return_value.pipe.assert_called_once()


def test_parse_page(storage_use_case):
    # Caso 1: página menor o igual a 0
    assert storage_use_case._parse_page(0) == 0
    assert storage_use_case._parse_page(-1) == 0

    # Caso 2: página mayor a 0
    assert storage_use_case._parse_page(1) == 0
    assert storage_use_case._parse_page(2) == 1
