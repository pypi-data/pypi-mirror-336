import pytest
from unittest.mock import MagicMock, patch
from reactivex import operators as op
from reactivex.testing import TestScheduler, ReactiveTest
from cqrs.core_api.src.storage.storage_exception import StorageException
from adapters.aws_s3.aws_s3_file import AwsS3File


@pytest.fixture
def aws_session():
    return MagicMock()


@pytest.fixture
def aws_s3_file(aws_session):
    return AwsS3File(aws_session)


def test_get_type(aws_s3_file):
    assert aws_s3_file.get_type() == "AWS-S3"


def test_list_bucket_name_empty(aws_s3_file):
    scheduler = TestScheduler()

    def on_next(value):
        pytest.fail("Expected error but got next value")

    def on_error(error):
        assert isinstance(error, StorageException)
        assert error.message == "El nombre del bucket es obligatorio"

    aws_s3_file.list("").pipe(
        op.subscribe_on(scheduler)
    ).subscribe(on_next=on_next, on_error=on_error)

    scheduler.start()


def test_list_bucket_success(aws_s3_file, aws_session):
    bucket_name = "test-bucket"
    aws_session.client().list_objects_v2.return_value = {
        "Contents": [{"Key": "file1.txt"}, {"Key": "file2.txt"}]
    }
    scheduler = TestScheduler()
    results = []

    def on_next(value):
        results.append(value)

    def on_error(error):
        pytest.fail(f"Unexpected error: {error}")

    aws_s3_file.list(bucket_name).pipe(
        op.subscribe_on(scheduler)
    ).subscribe(on_next=on_next, on_error=on_error)

    scheduler.start()
    assert results == ["file1.txt", "file2.txt"]


def test_list_bucket_error(aws_s3_file, aws_session):
    bucket_name = "test-bucket"
    aws_session.client().list_objects_v2.side_effect = Exception("Error listing bucket")
    scheduler = TestScheduler()

    def on_next(value):
        pytest.fail("Expected error but got next value")

    def on_error(error):
        assert isinstance(error, StorageException)
        assert error.message == "Error de procesamiento"

    aws_s3_file.list(bucket_name).pipe(
        op.subscribe_on(scheduler)
    ).subscribe(on_next=on_next, on_error=on_error)

    scheduler.start()
