import json
import pytest
from unittest.mock import MagicMock, patch
from collections import deque

from reactivex import of
from cqrs.core_api.src.event.event_error import EventError
from helpers.filequeue_fallback.src.file_queue_fallback import FileQueueFallBack


@pytest.fixture
def persistent_fs_queue():
    return MagicMock(spec=deque)


@pytest.fixture
def file_queue_fallback(persistent_fs_queue):
    return FileQueueFallBack(persistent_fs_queue)


def test_add_event_error(file_queue_fallback, persistent_fs_queue):
    event_error = EventError()
    result = file_queue_fallback.add(event_error)
    assert result is True
    assert persistent_fs_queue.append.called_once_with(
        json.dumps(event_error.__dict__))


def test_add_event_error_exception(file_queue_fallback, persistent_fs_queue, monkeypatch):
    persistent_fs_queue.append.side_effect = Exception("Mocked exception")

    result = file_queue_fallback.add(EventError())
    assert result is False


def test_receive_event_error(file_queue_fallback):
    event_error = EventError()
    event_error_observable = of(event_error)
    result = file_queue_fallback.receive_event_error(event_error_observable)
    assert result == json.dumps(event_error.__dict__)


def test_receive_json_event_error(file_queue_fallback, persistent_fs_queue):
    json_event_error = json.dumps({"error": "test"})
    json_event_error_observable = of(json_event_error)
    result = file_queue_fallback.receive_json_event_error(
        json_event_error_observable)
    assert result is True
    assert persistent_fs_queue.append.called_once_with(json_event_error)


def test_store_json(file_queue_fallback, persistent_fs_queue):
    json_event_error = json.dumps({"error": "test"})
    result = file_queue_fallback._FileQueueFallBack__store_json(
        json_event_error)
    assert result is True
    assert persistent_fs_queue.append.called_once_with(json_event_error)


def test_store_json_exception(file_queue_fallback, persistent_fs_queue):
    persistent_fs_queue.append.side_effect = Exception("Mocked exception")

    json_event_error = json.dumps({"error": "test"})
    result = file_queue_fallback._FileQueueFallBack__store_json(
        json_event_error)

    assert result is False
    assert len(persistent_fs_queue) == 0
