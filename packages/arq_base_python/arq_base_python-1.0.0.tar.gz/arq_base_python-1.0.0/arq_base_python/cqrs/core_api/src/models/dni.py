from dataclass_wizard import property_wizard
from typing_extensions import Annotated
from dataclasses import dataclass, field


@dataclass(init=False, eq=False)
class Dni(metaclass=property_wizard):
    tipo_identificacion: Annotated[str, field(default="")]
    identificacion: Annotated[str, field(default="")]

    __tipo_identificacion: str = field(repr=False, init=False)
    __identificacion: str = field(repr=False, init=False)

    def __init__(
        self,
        tipoIdentificacion: str = None,
        identificacion: str = None,
    ):
        self.__tipo_identificacion = tipoIdentificacion
        self.__identificacion = identificacion

    @property
    def tipo_identificacion(self) -> str:
        return self.__tipo_identificacion

    @tipo_identificacion.setter
    def tipo_identificacion(self, tipo_identificacion: str):
        self.__tipo_identificacion = str(tipo_identificacion)

    @property
    def identificacion(self) -> str:
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, identificacion: str):
        self.__identificacion = str(identificacion)

    def __dict__(self) -> dict:
        return {
            "tipoIdentificacion": self.tipo_identificacion,
            "identificacion": self.identificacion,
        }

    def __str__(self):
        # Construye la representación de cadena utilizando comillas dobles para los valores
        attributes_str = ", ".join(
            '{}="{}"'.format(k, v) for k, v in self.__dict__().items()
        )
        return "{}({})".format(self.__class__.__name__, attributes_str)
