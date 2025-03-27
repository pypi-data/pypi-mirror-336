import pytest
from unittest.mock import MagicMock, patch
from reactivex import operators as op
import reactivex
from reactivex.testing import TestScheduler, ReactiveTest
from arq_base_python.cqrs.core_api.src.storage.cloud_bucket import CloudBucket
from arq_base_python.cqrs.core_api.src.storage.storage_exception import StorageException
from arq_base_python.adapters.aws_s3.aws_s3_bucket import AwsS3Bucket


@pytest.fixture
def aws_session():
    return MagicMock()


@pytest.fixture
def cloud_bucket():
    return CloudBucket(name="test-bucket", region="us-east-1")


@pytest.fixture
def aws_s3_bucket(aws_session, cloud_bucket):
    return AwsS3Bucket(aws_session, cloud_bucket)


def test_get_info(aws_s3_bucket, cloud_bucket):
    assert aws_s3_bucket.get_info() == cloud_bucket


def test_create_bucket_exists(aws_s3_bucket, aws_session, cloud_bucket):
    # Arrange
    aws_session.client().head_bucket.return_value = {}
    scheduler = TestScheduler()

    def on_next(value):
        assert value is True

    def on_error(error):
        pytest.fail(f"Unexpected error: {error}")

    aws_s3_bucket.create(cloud_bucket).pipe(
        op.subscribe_on(scheduler)
    ).subscribe(on_next=on_next, on_error=on_error)

    scheduler.start()


def test_create_bucket_not_exists(aws_s3_bucket, aws_session, cloud_bucket):
    aws_session.client().head_bucket.side_effect = Exception("Bucket does not exist")
    aws_session.client().create_bucket.return_value = True
    scheduler = TestScheduler()

    def on_next(value):
        assert value is True

    def on_error(error):
        pytest.fail(f"Unexpected error: {error}")

    aws_s3_bucket.create(cloud_bucket).pipe(
        op.subscribe_on(scheduler)
    ).subscribe(on_next=on_next, on_error=on_error)

    scheduler.start()


def test_create_bucket_error(aws_s3_bucket, aws_session, cloud_bucket):
    aws_session.client().head_bucket.side_effect = Exception("Bucket does not exist")
    aws_session.client().create_bucket.side_effect = Exception("Error creating bucket")
    scheduler = TestScheduler()

    def on_next(value):
        pytest.fail("Expected error but got next value")

    def on_error(error):
        assert isinstance(error, StorageException)

    aws_s3_bucket.create(cloud_bucket).pipe(
        op.subscribe_on(scheduler)
    ).subscribe(on_next=on_next, on_error=on_error)

    scheduler.start()


def test_initialize_bucket_success(aws_s3_bucket, cloud_bucket):
    create_mock = MagicMock()
    aws_s3_bucket.create = create_mock
    create_mock.return_value = reactivex.of(True)

    aws_s3_bucket._initialize_bucket()

    create_mock.assert_called_once_with(cloud_bucket)


def test_initialize_bucket_invalid_bucket(aws_s3_bucket):
    aws_s3_bucket.bucket = CloudBucket(name="", region="us-east-1")

    with pytest.raises(StorageException) as excinfo:
        aws_s3_bucket._initialize_bucket()

    assert excinfo.value.message == "Repositorio no valido"
