import abc
from cqrs.core_api.src.models.common_body import CommonBody


class CoreMessagePublisher(abc.ABC):

    @abc.abstractmethod
    async def publish(self, var1: CommonBody):
        pass

    @abc.abstractmethod
    def publishError(self, var1: CommonBody):
        pass
