import abc
from typing import TypeVar, Generic

from arq_base_python.cqrs.core_api.src.models.command_submitted import CommandSubmitted
from arq_base_python.cqrs.core_api.src.models.event_submitted import EventSubmitted
from arq_base_python.cqrs.core_api.src.models.submittable import Submittable

T = TypeVar("T")


class MessageSerializer(abc.ABC):
    @abc.abstractmethod
    def serialize(self, var1: object) -> T:
        pass

    @abc.abstractmethod
    def parse_payload(self, var1: object, var2: type) -> T:
        pass

    @abc.abstractmethod
    def serialize_submittable(self, var1: Submittable) -> T:
        pass

    @abc.abstractmethod
    def to_command_submitted(self, var1: T) -> CommandSubmitted:
        pass

    @abc.abstractmethod
    def to_event_submitted(self, var1: T) -> EventSubmitted:
        pass
