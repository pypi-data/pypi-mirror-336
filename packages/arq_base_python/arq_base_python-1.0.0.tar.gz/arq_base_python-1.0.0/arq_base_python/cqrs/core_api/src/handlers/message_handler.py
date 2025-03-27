from typing import Callable, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')
R = TypeVar('R')


class MessageHandler(ABC, Generic[T, R]):

    @abstractmethod
    def __call__(self, t: T) -> [R]:
        pass
