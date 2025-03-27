from datetime import datetime
from dataclasses import dataclass, field
from dataclass_wizard import property_wizard
from typing_extensions import Annotated


@dataclass(init=False, eq=False)
class AplicacionEmisora(metaclass=property_wizard):
    id_aplicacion_emisora: Annotated[str, field(default="")]
    nombre_aplicacion_emisora: Annotated[str, field(default="")]
    id_transaccion_emisora: Annotated[str, field(default="")]
    fecha_transaccion: Annotated[str, field(default="")]

    __id_aplicacion_emisora: str = field(repr=False, init=False)
    __nombre_aplicacion_emisora: str = field(repr=False, init=False)
    __id_transaccion_emisora: str = field(repr=False, init=False)
    __fecha_transaccion: str = field(repr=False, init=False)

    def __init__(
        self,
        idAplicacionEmisora: str = None,
        nombreAplicacionEmisora: str = None,
        idTransaccionEmisora: str = None,
        fechaTransaccion: str = None,
    ):
        self.__id_aplicacion_emisora = idAplicacionEmisora
        self.__nombre_aplicacion_emisora = nombreAplicacionEmisora
        self.__id_transaccion_emisora = idTransaccionEmisora
        self.__fecha_transaccion = fechaTransaccion

    @property
    def id_aplicacion_emisora(self) -> str:
        return self.__id_aplicacion_emisora

    @id_aplicacion_emisora.setter
    def id_aplicacion_emisora(self, id_aplicacion_emisora: str):
        self.__id_aplicacion_emisora = str(id_aplicacion_emisora)

    @property
    def nombre_aplicacion_emisora(self) -> str:
        return self.__nombre_aplicacion_emisora

    @nombre_aplicacion_emisora.setter
    def nombre_aplicacion_emisora(self, nombre_aplicacion_emisora: str):
        self.__nombre_aplicacion_emisora = str(nombre_aplicacion_emisora)

    @property
    def id_transaccion_emisora(self) -> str:
        return self.__id_transaccion_emisora

    @id_transaccion_emisora.setter
    def id_transaccion_emisora(self, id_transaccion_emisora: str):
        self.__id_transaccion_emisora = str(id_transaccion_emisora)

    @property
    def fecha_transaccion(self) -> datetime:
        return self.__fecha_transaccion

    @fecha_transaccion.setter
    def fecha_transaccion(self, fecha_transaccion: datetime):
        self.__fecha_transaccion = fecha_transaccion

    def __dict__(self) -> dict:
        return {
            "idAplicacionEmisora": self.id_aplicacion_emisora,
            "nombreAplicacionEmisora": self.nombre_aplicacion_emisora,
            "idTransaccionEmisora": self.id_transaccion_emisora,
            "fechaTransaccion": self.fecha_transaccion,
        }

    def __str__(self):
        # Construye la representación de cadena utilizando comillas dobles para los valores
        attributes_str = ", ".join(
            '{}="{}"'.format(k, v) for k, v in self.__dict__().items()
        )
        return "{}({})".format(self.__class__.__name__, attributes_str)
