import logging
import reactivex

from reactivex import Observable, of
from reactivex import operators as op
from arq_base_python.cqrs.core_api.src.storage.file_service import FileService
from arq_base_python.cqrs.core_api.src.storage.storage_exception import StorageException


class AwsS3File(FileService):
    def __init__(self, aws_session):
        self.log = logging.getLogger(__name__)
        self.s3_client = aws_session.client("s3")

    def get_type(self) -> str:
        return "AWS-S3"

    def list(self, bucket_name: str) -> Observable[str]:
        if not bucket_name:
            return reactivex.throw(StorageException(
                "El nombre del bucket es obligatorio", "El nombre del bucket es obligatorio"))
        else:
            self.log.info(
                f"Obteniendo listado de archivos de {bucket_name}...")
            try:
                response = self.s3_client.list_objects_v2(Bucket=bucket_name)
                return reactivex.from_iterable(response.get("Contents", [])).pipe(
                    op.map(lambda obj: obj.get("Key")),
                )
            except Exception as e:
                return reactivex.throw(StorageException("Error de procesamiento", e))
