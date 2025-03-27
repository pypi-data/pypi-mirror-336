from dataclasses import dataclass, field
from typing_extensions import Annotated
from dataclass_wizard import property_wizard

from arq_base_python.jano.core.src.user_properties import UserProperties


@dataclass(init=False)
class RequestMetadata(metaclass=property_wizard):

    restrictions: Annotated[list, field(default=[])]
    commandId: Annotated[str, field(default="")]
    whitelisted: Annotated[bool, field(default="")]
    userProperties: Annotated[dict, field(default={})]
    encabezados: Annotated[list, field(default=[])]
    ip: Annotated[str, field(default="")]
    url: Annotated[str, field(default="")]
    method: Annotated[str, field(default="")]
    parameters: Annotated[list, field(default=[])]

    __restrictions: list = field(repr=False, init=False)
    __commandId: str = field(repr=False, init=False)
    __whitelisted: bool = field(repr=False, init=False)
    __userProperties: dict = field(repr=False, init=False)
    __encabezados: list = field(repr=False, init=False)
    __ip: str = field(repr=False, init=False)
    __url: str = field(repr=False, init=False)
    __method: str = field(repr=False, init=False)
    __parameters: list = field(repr=False, init=False)

    def __init__(
        self,
        restrictions: list = None,
        commandId: str = None,
        whitelisted: bool = False,
        userProperties: dict = {},
        encabezados: list = None,
        ip: str = None,
        url: str = None,
        method: str = None,
        parameters: list = None,
    ):
        self.__restrictions = restrictions if restrictions is not None else []
        self.__commandId = commandId
        self.__whitelisted = whitelisted
        self.__userProperties = UserProperties(**userProperties)
        self.__encabezados = encabezados if encabezados is not None else []
        self.__ip = ip
        self.__url = url
        self.__method = method
        self.__parameters = parameters if parameters is not None else []

    @property
    def restrictions(self) -> list:
        return self.__restrictions

    @restrictions.setter
    def restrictions(self, restrictions):
        self.__restrictions = restrictions

    @property
    def commandId(self) -> str:
        return self.__commandId

    @commandId.setter
    def commandId(self, commandId):
        self.__commandId = commandId

    @property
    def whitelisted(self) -> bool:
        return self.__whitelisted

    @whitelisted.setter
    def whitelisted(self, whitelisted):
        self.__whitelisted = whitelisted

    @property
    def userProperties(self) -> UserProperties:
        return self.__userProperties

    @userProperties.setter
    def userProperties(self, userProperties):
        self.__userProperties = userProperties

    @property
    def encabezados(self) -> list:
        return self.__encabezados

    @encabezados.setter
    def encabezados(self, encabezados):
        self.__encabezados = encabezados

    @property
    def ip(self) -> str:
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def method(self) -> str:
        return self.__method

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def parameters(self) -> list:
        return self.__parameters

    @parameters.setter
    def parameters(self, parameters):
        self.__parameters = parameters
