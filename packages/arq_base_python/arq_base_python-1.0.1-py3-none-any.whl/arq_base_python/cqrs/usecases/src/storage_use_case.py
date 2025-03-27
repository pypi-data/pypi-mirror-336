import logging

from reactivex import Observable, of, throw
from reactivex import operators as op
from arq_base_python.cqrs.core_api.src.storage.file_service import FileService
from arq_base_python.cqrs.core_api.src.storage.bucket_service import BucketService


class StorageUseCase:
    def __init__(self, file_service: FileService, bucket_service: BucketService):
        self.log = logging.getLogger(__name__)
        self.file_service = file_service
        self.bucket_service = bucket_service

    def list_by_page(self, page: int, page_size: int) -> Observable[str]:
        skip = self._parse_page(page) * page_size

        def _handle_error(e, src):
            self.log.error(f"Error listando archivos: {str(e)}")
            return throw((str(e)))
        return self.file_service.list(self.bucket_service.get_info().name).pipe(
            op.skip(skip),
            op.take(page_size),
            op.catch(_handle_error),
        )

    def list_all(self) -> Observable[str]:
        return self.list_by_page(0, 1000)

    def _parse_page(self, page: int) -> int:
        return 0 if page <= 0 else page - 1
