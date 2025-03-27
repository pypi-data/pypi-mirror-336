from datetime import date
from dataclass_wizard import property_wizard
from typing_extensions import Annotated
from dataclasses import dataclass, field


@dataclass(init=False)
class EventError(metaclass=property_wizard):
    id: Annotated[float, field(default=0)]
    name: Annotated[str, field(default="")]
    uuid: Annotated[str, field(default="")]
    json: Annotated[str, field(default="")]
    clase: Annotated[str, field(default="")]
    tipoDni: Annotated[str, field(default="")]
    dni: Annotated[str, field(default="")]
    fechaEvento: Annotated[date, field()]
    errorDescription: Annotated[str, field(default="")]

    __id: float = field(repr=False, init=False)
    __name: str = field(repr=False, init=False)
    __uuid: str = field(repr=False, init=False)
    __json: str = field(repr=False, init=False)
    __clase: str = field(repr=False, init=False)
    __tipoDni: str = field(repr=False, init=False)
    __dni: str = field(repr=False, init=False)
    __fechaEvento: date = field(repr=False, init=False)
    __errorDescription: str = field(repr=False, init=False)

    def __init__(
        self,
        id: float = None,
        name: str = None,
        uuid: str = None,
        json: str = None,
        clase: str = None,
        tipoDni: str = None,
        dni: str = None,
        fechaEvento: date = None,
        errorDescription: str = None,
    ):
        self.__id = id
        self.__name = name
        self.__uuid = uuid
        self.__json = json
        self.__clase = clase
        self.__tipoDni = tipoDni
        self.__dni = dni
        self.__fechaEvento = fechaEvento
        self.__errorDescription = errorDescription

    @property
    def id(self) -> float:
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def uuid(self) -> str:
        return self.__uuid

    @uuid.setter
    def uuid(self, uuid):
        self.__uuid = uuid

    @property
    def json(self) -> str:
        return self.__json

    @json.setter
    def json(self, json):
        self.__json = json

    @property
    def clase(self) -> str:
        return self.__clase

    @clase.setter
    def clase(self, clase):
        self.__clase = clase

    @property
    def tipoDni(self) -> str:
        return self.__tipoDni

    @tipoDni.setter
    def tipoDni(self, tipoDni):
        self.__tipoDni = tipoDni

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, dni):
        self.__dni = dni

    @property
    def fechaEvento(self) -> date:
        return self.__fechaEvento

    @fechaEvento.setter
    def fechaEvento(self, fechaEvento):
        self.__fechaEvento = fechaEvento

    @property
    def errorDescription(self) -> str:
        return self.__errorDescription

    @errorDescription.setter
    def errorDescription(self, errorDescription):
        self.__errorDescription = errorDescription
