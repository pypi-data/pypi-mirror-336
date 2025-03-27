import logging
import reactivex
from reactivex import Observable
from arq_base_python.cqrs.core_api.src.storage.bucket_service import BucketService
from arq_base_python.cqrs.core_api.src.storage.cloud_bucket import CloudBucket
from arq_base_python.cqrs.core_api.src.storage.storage_exception import StorageException


class AwsS3Bucket(BucketService):
    def __init__(self, aws_session: object, bucket: CloudBucket):
        self.log = logging.getLogger(__name__)
        self.s3_client = aws_session.client("s3")
        self.bucket = bucket

    def _initialize_bucket(self):
        self.log.info("Creando objeto bucketService...")
        if self.bucket and self.bucket.name not in ["", None]:
            self.create(self.bucket).subscribe(
                on_next=lambda v: self.log.info(
                    f"Fin proceso validacion/aprovisionamiento del bucket s3"),
                on_error=lambda e: self.log.error(
                    f"El proceso de creacion del bucket s3 no fue exitoso. Si el usuario de AWS asignado a la aplicacion no tiene permisos para auto-crear el bucket, debe solicitar la creacion del mismo al equipo de operacion, error: {str(e)}"),
            )
        else:
            raise StorageException(
                "Repositorio no valido", "El nombre del bucket para almacenamiento en nube no es valido.")

    def get_info(self) -> CloudBucket:
        return self.bucket

    def create(self, bucket: CloudBucket) -> Observable[bool]:
        self.bucket = bucket

        def supplier():
            resultado = False
            try:
                self.s3_client.head_bucket(Bucket=bucket.name)
                self.log.info(f"Bucket {bucket.name} ya existe")
                resultado = True
            except Exception as e:
                resultado = False

            if not resultado:
                try:
                    self.s3_client.create_bucket(Bucket=bucket.name)
                    self.log.info(f"Bucket S3 {bucket.name} creado")
                    resultado = True
                except Exception as e:
                    raise StorageException("Error creando repositorio", e)

            return resultado

        return reactivex.defer(lambda scheduler: reactivex.of(supplier()))
