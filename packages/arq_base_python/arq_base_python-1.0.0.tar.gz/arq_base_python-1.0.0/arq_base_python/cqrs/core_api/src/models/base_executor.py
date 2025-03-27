import abc
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from typing_extensions import Annotated
from dataclass_wizard import property_wizard


@dataclass(init=False)
class BaseExecutor(abc.ABC, metaclass=property_wizard):
    @abc.abstractmethod
    def execute(self, var1):
        pass
