import abc
from typing import TypeVar, Generic
from arq_base_python.cqrs.core_api.src.jms.base_message import BaseMessage

T = TypeVar("T")


class ConcreteSender(
    Generic[T],
    abc.ABC,
):
    @abc.abstractmethod
    async def send(self, var1: str, var2: BaseMessage[T]):
        pass

    @abc.abstractmethod
    async def send_error(self, var1: str, var2: BaseMessage[T]):
        pass
