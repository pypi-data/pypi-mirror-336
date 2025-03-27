from dataclass_wizard import property_wizard
from typing_extensions import Annotated
from dataclasses import dataclass, field


@dataclass(init=False, eq=False)
class Usuario(metaclass=property_wizard):
    dni: Annotated[str, field(default="")]
    ip: Annotated[str, field(default="")]
    nombre: Annotated[str, field(default="")]
    canal: Annotated[str, field(default="")]
    telefono: Annotated[str, field(default="")]
    id_session: Annotated[str, field(default="")]

    __dni: str = field(repr=False, init=False)
    __ip: str = field(repr=False, init=False)
    __nombre: str = field(repr=False, init=False)
    __canal: str = field(repr=False, init=False)
    __telefono: str = field(repr=False, init=False)
    __id_session: str = field(repr=False, init=False)

    def __init__(
        self,
        dni: str = None,
        ip: str = None,
        nombre: str = None,
        canal: str = None,
        telefono: str = None,
        idSession: str = None,
    ):
        self.__dni = dni
        self.__ip = ip
        self.__nombre = nombre
        self.__canal = canal
        self.__telefono = telefono
        self.__id_session = idSession

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, dni: str):
        self.__dni = str(dni)

    @property
    def ip(self) -> str:
        return self.__ip

    @ip.setter
    def ip(self, ip: str):
        self.__ip = str(ip)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str):
        self.__nombre = str(nombre)

    @property
    def canal(self) -> str:
        return self.__canal

    @canal.setter
    def canal(self, canal: str):
        self.__canal = str(canal)

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono: str):
        self.__telefono = str(telefono)

    @property
    def id_session(self) -> str:
        return self.__id_session

    @id_session.setter
    def id_session(self, id_session: str):
        self.__id_session = str(id_session)

    def __dict__(self) -> dict:
        return {
            "dni": self.dni,
            "ip": self.ip,
            "nombre": self.nombre,
            "canal": self.canal,
            "telefono": self.telefono,
            "idSession": self.id_session,
        }

    def __str__(self):
        # Construye la representación de cadena utilizando comillas dobles para los valores
        attributes_str = ", ".join(
            '{}="{}"'.format(k, v) for k, v in self.__dict__().items()
        )
        return "{}({})".format(self.__class__.__name__, attributes_str)
