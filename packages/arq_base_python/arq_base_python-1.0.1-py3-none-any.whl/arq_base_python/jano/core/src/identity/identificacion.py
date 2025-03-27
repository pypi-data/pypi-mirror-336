import re

from dataclass_wizard import property_wizard
from typing_extensions import Annotated
from dataclasses import dataclass, field


@dataclass(init=False)
class Identificacion(metaclass=property_wizard):

    IDENTIFICACION_PATTERN = "^([a-zA-Z]+)([ _\\W])*([0-9]+)$"
    id: Annotated[str, field()]
    tipoId: Annotated[str, field()]

    __id: str = field(repr=False, init=False)
    __tipoId: str = field(repr=False, init=False)

    def __init__(self, id: str = None, tipoId: str = None, identificacion: str = ""):
        self.__id = id
        self.__tipoId = tipoId

        matcherThis = re.match(self.IDENTIFICACION_PATTERN, identificacion)

        if matcherThis:
            self.id = matcherThis[3]
            self.tipoId = matcherThis[1]

    def __repr__(self):
        return f"{self.tipoId}-{self.id}"

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def tipoId(self) -> str:
        return self.__tipoId

    @tipoId.setter
    def tipoId(self, tipoId):
        self.__tipoId = tipoId
