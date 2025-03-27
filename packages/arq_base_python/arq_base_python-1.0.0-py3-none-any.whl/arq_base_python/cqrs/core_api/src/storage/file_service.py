from abc import ABC, abstractmethod
from reactivex import Observable


class FileService(ABC):
    @abstractmethod
    def get_type(self) -> str:
        pass

    @abstractmethod
    def list(self, var1: str) -> Observable[str]:
        pass
