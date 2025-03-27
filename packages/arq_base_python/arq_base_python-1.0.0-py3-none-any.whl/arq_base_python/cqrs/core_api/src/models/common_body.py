import abc
from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Generic, TypeVar
from typing_extensions import Annotated
from dataclass_wizard import property_wizard

from cqrs.core_api.src.models.aplicacion_emisora import (
    AplicacionEmisora,
)
from cqrs.core_api.src.models.aplicacion_origen import (
    AplicacionOrigen,
)
from cqrs.core_api.src.models.usuario import Usuario
from cqrs.core_api.src.models.dni import Dni

T = TypeVar("T")


@dataclass(init=False, eq=False)
class CommonBody(abc.ABC, Generic[T], metaclass=property_wizard):
    id: Annotated[str, field(default="")]
    id_trazabilidad: Annotated[str, field(default="")]
    nombre: Annotated[str, field(default="")]
    version: Annotated[str, field(default="")]
    aplicacion_emisora: Annotated[dict, field(default={})]  # AplicacionEmisora
    aplicacion_origen: Annotated[dict, field(default={})]  # AplicacionOrigen
    usuario: Annotated[dict, field(default={})]  # Usuario
    dni: Annotated[dict, field(default={})]  # Dni
    timestamp: Annotated[int, field(default=0)]
    payload: Annotated[T, field()]

    __id: str = field(repr=False, init=False)
    __id_trazabilidad: str = field(repr=False, init=False)
    __nombre: str = field(repr=False, init=False)
    __version: str = field(repr=False, init=False)
    __aplicacion_emisora: dict = field(repr=False, init=False)
    __aplicacion_origen: dict = field(repr=False, init=False)
    __usuario: dict = field(repr=False, init=False)
    __dni: dict = field(repr=False, init=False)
    __timestamp: int = field(repr=False, init=False)
    __payload: T = field(repr=False, init=False)

    def __init__(
        self,
        id: str = None,
        idTrazabilidad: str = None,
        nombre: str = None,
        version: str = None,
        aplicacionEmisora: dict = None,
        aplicacionOrigen: dict = None,
        usuario: dict = None,
        dni: dict = None,
        timestamp: int = None,
        payload: T = None,
    ):
        self.__id = id
        self.__id_trazabilidad = idTrazabilidad
        self.__nombre = nombre
        self.__version = version
        self.__aplicacion_emisora = AplicacionEmisora(
            **aplicacionEmisora) if aplicacionEmisora else None
        self.__aplicacion_origen = AplicacionOrigen(
            **aplicacionOrigen) if aplicacionOrigen else None
        self.__usuario = Usuario(**usuario) if usuario else None
        self.__dni = Dni(**dni) if dni else None
        self.__timestamp = timestamp
        self.__payload = payload

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: str):
        self.__id = str(id)

    @property
    def id_trazabilidad(self) -> str:
        return self.__id_trazabilidad

    @id_trazabilidad.setter
    def id_trazabilidad(self, id_trazabilidad: str):
        self.__id_trazabilidad = str(id_trazabilidad)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str):
        self.__nombre = str(nombre)

    @property
    def version(self) -> str:
        return self.__version

    @version.setter
    def version(self, version: str):
        self.__version = str(version)

    @property
    def aplicacion_emisora(self) -> AplicacionEmisora:
        return self.__aplicacion_emisora

    @aplicacion_emisora.setter
    def aplicacion_emisora(self, aplicacion_emisora: AplicacionEmisora):
        self.__aplicacion_emisora = aplicacion_emisora

    @property
    def aplicacion_origen(self) -> AplicacionOrigen:
        return self.__aplicacion_origen

    @aplicacion_origen.setter
    def aplicacion_origen(self, aplicacion_origen: AplicacionOrigen):
        self.__aplicacion_origen = aplicacion_origen

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @usuario.setter
    def usuario(self, usuario: Usuario):
        self.__usuario = usuario

    @property
    def dni(self) -> Dni:
        return self.__dni

    @dni.setter
    def dni(self, dni: Dni):
        self.__dni = dni

    @property
    def timestamp(self) -> int:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp: int):
        self.__timestamp = int(timestamp)

    @property
    def payload(self) -> T:
        return self.__payload

    @payload.setter
    def payload(self, payload: T):
        self.__payload = payload

    def _serialize_payload(self):
        if isinstance(self.payload, dict):
            return self.payload
        elif isinstance(self.payload, BaseModel):
            return self.payload.model_dump(mode='json')
        elif hasattr(self.payload, '__dict__'):
            return self.payload.__dict__
        else:
            return self.payload

    def __dict__(self):
        return {
            "id": self.id,
            "idTrazabilidad": self.id_trazabilidad,
            "nombre": self.nombre,
            "version": self.version,
            "aplicacionEmisora": self.aplicacion_emisora,
            "aplicacionOrigen": self.aplicacion_origen,
            "usuario": self.usuario,
            "dni": self.dni,
            "timestamp": self.timestamp,
            "payload": self._serialize_payload(),
        }
