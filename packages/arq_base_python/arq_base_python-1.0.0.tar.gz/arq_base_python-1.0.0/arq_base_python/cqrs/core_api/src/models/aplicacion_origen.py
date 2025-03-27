from dataclasses import dataclass, field
from typing_extensions import Annotated
from dataclass_wizard import property_wizard


@dataclass(init=False, eq=False)
class AplicacionOrigen(metaclass=property_wizard):

    id_aplicacion_origen: Annotated[str, field(default="")]
    nombre_aplicacion_origen: Annotated[str, field(default="")]

    __id_aplicacion_origen: str = field(repr=False, init=False)
    __nombre_aplicacion_origen: str = field(repr=False, init=False)

    def __init__(
        self,
        idAplicacionOrigen: str = None,
        nombreAplicacionOrigen: str = None,
    ):
        self.__id_aplicacion_origen = idAplicacionOrigen
        self.__nombre_aplicacion_origen = nombreAplicacionOrigen

    @property
    def id_aplicacion_origen(self) -> str:
        return self.__id_aplicacion_origen

    @id_aplicacion_origen.setter
    def id_aplicacion_origen(self, id_aplicacion_origen: str):
        self.__id_aplicacion_origen = str(id_aplicacion_origen)

    @property
    def nombre_aplicacion_origen(self) -> str:
        return self.__nombre_aplicacion_origen

    @nombre_aplicacion_origen.setter
    def nombre_aplicacion_origen(self, nombre_aplicacion_origen: str):
        self.__nombre_aplicacion_origen = str(nombre_aplicacion_origen)

    def __dict__(self) -> dict:
        return {
            "idAplicacionOrigen": self.id_aplicacion_origen,
            "nombreAplicacionOrigen": self.nombre_aplicacion_origen,
        }

    def __str__(self):
        # Construye la representación de cadena utilizando comillas dobles para los valores
        attributes_str = ", ".join(
            '{}="{}"'.format(k, v) for k, v in self.__dict__().items()
        )
        return "{}({})".format(self.__class__.__name__, attributes_str)
