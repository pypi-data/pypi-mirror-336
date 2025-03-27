from typing import TypeVar
from dataclasses import dataclass

from cqrs.core_api.src.models.common_body import CommonBody

T = TypeVar("T")


@dataclass(init=False, eq=False)
class Command(CommonBody[T]):
    def __dict__(self):
        return super().__dict__()

    def __repr__(self):
        """Remove this method to get all fields in representation"""
        return f"Comando(nombre={self.nombre})"
