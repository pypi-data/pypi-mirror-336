from fastapi import HTTPException, status
import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Field, SQLModel
from reactivex import Observable, of
from data.reactive_repository_adapter.src.reactive_adapter import ReactiveAdapter


class TestEntity(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str


@pytest.fixture
def entity():
    return TestEntity(id=1, name="Test Entity")


@pytest.fixture
def reactive_adapter():
    return ReactiveAdapter(TestEntity)


def test_all(reactive_adapter):
    with patch('data.reactive_repository_adapter.src.reactive_adapter.Session') as mock_session:
        mock_session.return_value.__enter__.return_value.exec.return_value.all.return_value = [
            TestEntity(id=1, name="Test Entity")]
        result = reactive_adapter.all()
        assert isinstance(result, Observable)
        items = [result.run()]
        assert len(items) == 1
        assert items[0].id == 1
        assert items[0].name == "Test Entity"
        assert items[0].__class__ == TestEntity


def test_save(reactive_adapter, entity):
    with patch('data.reactive_repository_adapter.src.reactive_adapter.Session') as mock_session:
        mock_session.return_value.__enter__.return_value.add.return_value = None
        mock_session.return_value.__enter__.return_value.commit.return_value = None
        mock_session.return_value.__enter__.return_value.refresh.return_value = None
        result = reactive_adapter.save(entity)
        assert isinstance(result, Observable)
        items = []
        result.subscribe(on_next=lambda x: items.append(x))
        assert len(items) == 1
        assert items[0].id == 1
        assert items[0].name == "Test Entity"


def test_update_existing(reactive_adapter, entity):
    with patch('data.reactive_repository_adapter.src.reactive_adapter.Session') as mock_session:
        mock_session.return_value.__enter__.return_value.get.return_value = entity
        mock_session.return_value.__enter__.return_value.commit.return_value = None
        mock_session.return_value.__enter__.return_value.refresh.return_value = None
        result = reactive_adapter.update(entity)
        assert isinstance(result, Observable)
        items = []
        result.subscribe(on_next=lambda x: items.append(x))
        assert len(items) == 1
        assert items[0].id == 1
        assert items[0].name == "Test Entity"


def test_update_non_existing(reactive_adapter, entity):
    with patch('data.reactive_repository_adapter.src.reactive_adapter.Session') as mock_session, \
            patch('data.reactive_repository_adapter.src.reactive_adapter.ReactiveAdapter.save') as mock_save:
        mock_session.return_value.__enter__.return_value.get.return_value = None
        mock_session.return_value.__enter__.return_value.add.return_value = None
        mock_session.return_value.__enter__.return_value.commit.return_value = None
        mock_session.return_value.__enter__.return_value.refresh.return_value = None
        mock_save.return_value = of(entity)
        result = reactive_adapter.update(entity)

        assert isinstance(result, Observable)
        item = result.run()
        assert item is not None
        assert item == entity
        assert mock_save.called_once_with(entity)


def test_delete_existing(reactive_adapter):
    with patch('data.reactive_repository_adapter.src.reactive_adapter.Session') as mock_session:
        mock_session.return_value.__enter__.return_value.get.return_value = TestEntity(
            id=1, name="Test Entity")
        mock_session.return_value.__enter__.return_value.delete.return_value = None
        mock_session.return_value.__enter__.return_value.commit.return_value = None
        result = reactive_adapter.delete(1)
        assert isinstance(result, Observable)
        deleted = result.run()
        assert deleted is None


def test_delete_non_existing(reactive_adapter):
    with patch('data.reactive_repository_adapter.src.reactive_adapter.Session') as mock_session:
        mock_session.return_value.__enter__.return_value.get.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            reactive_adapter.delete(1).subscribe()
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == "TestEntity with id 1 not found"
