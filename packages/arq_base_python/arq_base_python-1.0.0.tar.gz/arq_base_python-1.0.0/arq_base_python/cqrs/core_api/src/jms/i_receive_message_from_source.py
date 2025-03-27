import abc
from dataclasses import dataclass
from dataclass_wizard import property_wizard

from cqrs.core_api.src.jms.base_message import BaseMessage


@dataclass(init=False)
class IReceiveMessageFromSource(abc.ABC, metaclass=property_wizard):
    @abc.abstractmethod
    def processMessage(self, var1: BaseMessage):
        pass
