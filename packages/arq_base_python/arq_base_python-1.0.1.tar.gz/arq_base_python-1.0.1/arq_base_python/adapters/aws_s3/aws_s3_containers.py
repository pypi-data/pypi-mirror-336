from dependency_injector import containers, providers

from arq_base_python.adapters.aws_s3.aws_s3_file import AwsS3File
from arq_base_python.adapters.aws_s3.aws_s3_bucket import AwsS3Bucket
from arq_base_python.containers.aws_containers import AWSSessionContainer
from arq_base_python.cqrs.core_api.src.storage.cloud_bucket import CloudBucket


class AwsS3Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["application.yml"])

    cloud_bucket = providers.Singleton(
        CloudBucket,
        name=config.storage.cloud.bucket,
        region=config.cloud.aws.region.static,
    )

    aws_s3_file = providers.Factory(
        AwsS3File,
        aws_session=AWSSessionContainer.session,
    )

    aws_s3_bucket = providers.Factory(
        AwsS3Bucket,
        aws_session=AWSSessionContainer.session,
        bucket=cloud_bucket,
    )
