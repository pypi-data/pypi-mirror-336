from dependency_injector import containers, providers
from entrypoints_base.storage_rest_api.fileapi.storage_handler_v2 import StorageHandlerV2
from cqrs.usecases.src.storage_use_case import StorageUseCase
from adapters.aws_s3.aws_s3_containers import AwsS3Container


class StorageContainer(containers.DeclarativeContainer):

    storage_use_case: StorageUseCase = providers.Factory(
        StorageUseCase,
        file_service=AwsS3Container().aws_s3_file,
        bucket_service=AwsS3Container().aws_s3_bucket,
    )

    storage_handler_v2: StorageHandlerV2 = providers.Factory(
        StorageHandlerV2,
        storage_use_case=storage_use_case,
    )
