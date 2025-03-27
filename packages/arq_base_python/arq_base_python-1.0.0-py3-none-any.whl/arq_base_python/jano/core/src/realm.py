from dataclasses import dataclass, field
from typing_extensions import Annotated
from dataclass_wizard import property_wizard


@dataclass
class Realm(metaclass=property_wizard):
    EMPLEADOS: Annotated[bool, field(default=False)]
    CLIENTE_AFILIADO: Annotated[bool, field(default=False)]
    CLIENTE_EMPRESA: Annotated[bool, field(default=False)]
    TERCERO: Annotated[bool, field(default=False)]
    APLICACION: Annotated[bool, field(default=False)]

    __EMPLEADOS: bool = field(repr=False, init=False)
    __CLIENTE_AFILIADO: bool = field(repr=False, init=False)
    __CLIENTE_EMPRESA: bool = field(repr=False, init=False)
    __TERCERO: bool = field(repr=False, init=False)
    __APLICACION: bool = field(repr=False, init=False)

    def __init__(self):
        EMPLEADOS: bool = False
        CLIENTE_AFILIADO: bool = False
        CLIENTE_EMPRESA: bool = False
        TERCERO: bool = False
        APLICACION: bool = False

        self.__EMPLEADOS = EMPLEADOS
        self.__CLIENTE_AFILIADO = CLIENTE_AFILIADO
        self.__CLIENTE_EMPRESA = CLIENTE_EMPRESA
        self.__TERCERO = TERCERO
        self.__APLICACION = APLICACION

    @property
    def EMPLEADOS(self) -> bool:
        return self.__EMPLEADOS

    @property
    def CLIENTE_AFILIADO(self) -> bool:
        return self.__CLIENTE_AFILIADO

    @property
    def CLIENTE_EMPRESA(self) -> bool:
        return self.__CLIENTE_EMPRESA

    @property
    def TERCERO(self) -> bool:
        return self.__TERCERO

    @property
    def APLICACION(self) -> bool:
        return self.__APLICACION
