import logging
from dependency_injector.wiring import Provide, inject
from arq_base_python.adapters.aws_s3.aws_s3_bucket import AwsS3Bucket
from arq_base_python.containers.application_container import Application


@inject
class S3Init:
    def __init__(self,
                 aws_s3_bucket: AwsS3Bucket = Provide[Application.aws_s3_container.aws_s3_bucket]):
        self.log = logging.getLogger(__name__)
        self.aws_s3_bucket = aws_s3_bucket
        self.aws_s3_bucket._initialize_bucket()
