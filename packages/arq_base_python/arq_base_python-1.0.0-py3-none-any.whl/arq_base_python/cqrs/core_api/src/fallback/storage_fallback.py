import abc
from dataclasses import dataclass
from dataclass_wizard import property_wizard

from cqrs.core_api.src.event.event_error import EventError


@dataclass(init=False)
class StorageFallback(abc.ABC, metaclass=property_wizard):

    @abc.abstractmethod
    def add(self, var1: EventError):
        pass
