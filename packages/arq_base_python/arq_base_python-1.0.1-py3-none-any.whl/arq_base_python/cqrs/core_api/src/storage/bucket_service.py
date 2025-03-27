from abc import ABC, abstractmethod
from reactivex import Observable

from arq_base_python.cqrs.core_api.src.storage.cloud_bucket import CloudBucket


class BucketService(ABC):
    @abstractmethod
    def get_info(self) -> CloudBucket:
        pass

    @abstractmethod
    def create(self, var1: CloudBucket) -> Observable[bool]:
        pass
