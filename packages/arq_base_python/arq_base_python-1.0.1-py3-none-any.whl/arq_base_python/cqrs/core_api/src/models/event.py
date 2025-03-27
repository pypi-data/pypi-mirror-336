from typing import TypeVar
from typing_extensions import Annotated
from dataclasses import dataclass, field
from dataclass_wizard import property_wizard
import inspect

from arq_base_python.cqrs.core_api.src.models.common_body import CommonBody

T = TypeVar("T")


@dataclass(init=False, repr=False, eq=False)
class Event(CommonBody[T], metaclass=property_wizard):
    idComando: Annotated[str, field(default="")]
    resultado: Annotated[str, field(default="")]
    eventScope: Annotated[str, field(default="")]

    __idComando: str = field(repr=False, init=False)
    __resultado: str = field(repr=False, init=False)
    __eventScope: str = field(repr=False, init=False)

    def __init__(self, **data):
        # For receiving CommonBody parameters in the constructor
        common_body_params = inspect.signature(CommonBody).parameters
        # Filter out parameters for CommonBody and Event
        common_body_data = {k: data[k]
                            for k in data if k in common_body_params}
        super().__init__(**common_body_data)

        self.idComando = data.get("idComando", "")
        self.resultado = data.get("resultado", "")
        self.eventScope = data.get("eventScope", "")

    @property
    def idComando(self) -> str:
        return self.__idComando

    @idComando.setter
    def idComando(self, id: str):
        self.__idComando = str(id)

    @property
    def resultado(self) -> str:
        return self.__resultado

    @resultado.setter
    def resultado(self, resultado: str):
        self.__resultado = str(resultado)

    @property
    def eventScope(self) -> str:
        return self.__eventScope

    @eventScope.setter
    def eventScope(self, eventScope: str):
        self.__eventScope = str(eventScope)

    def __repr__(self) -> str:
        return f"Event(nombre={self.nombre}, idComando={self.idComando}, resultado={self.resultado}, eventScope={self.eventScope})"

    def __dict__(self) -> dict:
        return {
            **super().__dict__(),
            "idComando": self.idComando,
            "resultado": self.resultado,
            "eventScope": self.eventScope,
        }
