from typing import TypedDict
from unittest import mock
from reactivex import of
from reactivex.operators import to_list
from entrypoints_base.storage_rest_api.fileapi.storage_handler_v2 import StorageHandlerV2
from cqrs.usecases.src.storage_use_case import StorageUseCase


class ResponseType(TypedDict):
    files: list[str]
    pageSize: int
    page: int
    commandId: str
    parentId: str


def test_get_keys_with_page():
    # Arrange
    storage_use_case = mock.Mock(spec=StorageUseCase)
    handler = StorageHandlerV2(storage_use_case)
    page = 1
    expected_result = ["file1", "file2"]
    storage_use_case.list_by_page.return_value = of(*expected_result)

    # Act
    result: ResponseType = handler.list_files_in_repository(page).run()

    # Assert
    assert result["files"] == expected_result
    assert result["pageSize"] == handler.PAGE_SIZE
    storage_use_case.list_by_page.assert_called_once_with(
        page, handler.PAGE_SIZE)


def test_get_keys_without_page():
    # Arrange
    storage_use_case = mock.Mock(spec=StorageUseCase)
    handler = StorageHandlerV2(storage_use_case)
    page = None
    expected_result = ["file1", "file2"]
    storage_use_case.list_all.return_value = of(*expected_result)

    # Act
    result: ResponseType = handler.list_files_in_repository(page).run()

    # Assert
    assert result["files"] == expected_result
    assert result["pageSize"] == handler.PAGE_SIZE
    storage_use_case.list_all.assert_called_once()
