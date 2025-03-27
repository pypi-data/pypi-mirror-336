import abc

from arq_base_python.cqrs.core_api.src.models.event import Event
from arq_base_python.cqrs.core_api.src.models.submittable import Submittable


class IMessagePublisher(abc.ABC):
    @abc.abstractmethod
    async def publish(self, var1: Submittable):
        pass

    @abc.abstractmethod
    def publish_for_log(self, var1: Submittable) -> str:
        pass

    @abc.abstractmethod
    def initialize_event_properties(self, var1: Event, var2: Submittable) -> str:
        pass
