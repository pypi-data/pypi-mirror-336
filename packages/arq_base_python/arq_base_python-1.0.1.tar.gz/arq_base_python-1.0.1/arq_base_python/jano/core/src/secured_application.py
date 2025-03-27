from dataclasses import dataclass, field
from typing_extensions import Annotated
from dataclass_wizard import property_wizard


@dataclass(init=False)
class SecuredApplication(metaclass=property_wizard):

    id_app_proteccion: Annotated[int, field(default="")]
    name: Annotated[str, field()]
    white_listed_ips: Annotated[str, field()]
    allow_origin: Annotated[str, field()]
    allow_headers: Annotated[str, field()]
    expose_headers: Annotated[str, field()]
    bus_base_url: Annotated[str, field()]
    validate_token_ip: Annotated[bool, field()]
    file_queue: Annotated[str, field()]
    file_repo: Annotated[str, field()]
    jano_enabled: Annotated[bool, field(default=True)]

    __id_app_proteccion: int = field(repr=False, init=False)
    __name: str = field(repr=False, init=False)
    __white_listed_ips: str = field(repr=False, init=False)
    __allow_origin: str = field(repr=False, init=False)
    __allow_headers: str = field(repr=False, init=False)
    __expose_headers: str = field(repr=False, init=False)
    __bus_base_url: str = field(repr=False, init=False)
    __validate_token_ip: bool = field(repr=False, init=False)
    __file_queue: str = field(repr=False, init=False)
    __file_repo: str = field(repr=False, init=False)
    __jano_enabled: bool = field(repr=False, init=False)

    # scopesDeAplicacion: Annotated[list, field(default=[])]
    # __scopesDeAplicacion: list = field(repr=False, init=False)

    # audiences: Annotated[list, field(default=[])]
    # __audiences: list = field(repr=False, init=False)

    def __init__(
        self,
        config: dict = None,
        id_app_proteccion: int = 0,
        name: str = "",
        white_listed_ips: str = "",
        allow_origin: str = "",
        allow_headers: str = "",
        expose_headers: str = "",
        bus_base_url: str = "",
        validate_token_ip: bool = False,
        file_queue: str = "",
        file_repo: str = "",
        jano_enabled: bool = True,
    ):
        self.config = config if config is not None else {}
        self.__id_app_proteccion = self.config.get(
            "idAppProteccion", id_app_proteccion)
        self.__name = self.config.get("name", name)
        self.__white_listed_ips = self.config.get(
            "whiteListedIps", white_listed_ips)
        self.__allow_origin = self.config.get("allowOrigin", allow_origin)
        self.__allow_headers = self.config.get("allowHeaders", allow_headers)
        self.__expose_headers = self.config.get(
            "exposeHeaders", expose_headers)
        self.__bus_base_url = self.config.get("busBaseUrl", bus_base_url)
        self.__validate_token_ip = self.config.get(
            "validateTokenIP", validate_token_ip)
        self.__file_queue = self.config.get("fileQueue", file_queue)
        self.__file_repo = self.config.get("fileRepo", file_repo)
        self.__jano_enabled = self.config.get("janoEnabled", jano_enabled)

    # def add_application_scope(self, scope):
    #     if scope is not None:
    #         if scope not in self.__scopesDeAplicacion:
    #             self.__scopesDeAplicacion.append(scope)

    # @property
    # def getApplicationScopes(self):
    #     return self.__scopesDeAplicacion

    # def getApplicationScope(self, authenticationScope):
    #     scopes = list(
    #         filter(
    #             lambda s: s.getAuthenticationScope() == authenticationScope,
    #             self.scopesDeAplicacion,
    #         )
    #     )
    #     return scopes[0] if scopes else None

    @property
    def id_app_proteccion(self) -> int:
        return self.__id_app_proteccion

    @id_app_proteccion.setter
    def id_app_proteccion(self, id_app_proteccion: int) -> None:
        self.__id_app_proteccion = int(id_app_proteccion)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name) -> None:
        self.__name = str(name)

    @property
    def white_listed_ips(self) -> str:
        return self.__white_listed_ips

    @white_listed_ips.setter
    def white_listed_ips(self, white_listed_ips) -> None:
        self.__white_listed_ips = str(white_listed_ips)

    @property
    def allow_origin(self) -> str:
        return self.__allow_origin

    @allow_origin.setter
    def allow_origin(self, allow_origin) -> None:
        self.__allow_origin = allow_origin

    @property
    def allow_headers(self) -> str:
        return self.__allow_headers

    @allow_headers.setter
    def allow_headers(self, allow_headers) -> None:
        self.__allow_headers = allow_headers

    @property
    def expose_headers(self) -> str:
        return self.__expose_headers

    @expose_headers.setter
    def expose_headers(self, expose_headers) -> None:
        self.__expose_headers = expose_headers

    @property
    def bus_base_url(self) -> str:
        return self.__bus_base_url

    @bus_base_url.setter
    def bus_base_url(self, bus_base_url) -> None:
        self.__bus_base_url = bus_base_url

    @property
    def validate_token_ip(self) -> bool:
        return self.__validate_token_ip

    @validate_token_ip.setter
    def validate_token_ip(self, validate_token_ip) -> None:
        self.__validate_token_ip = validate_token_ip

    @property
    def file_queue(self) -> str:
        return self.__file_queue

    @file_queue.setter
    def file_queue(self, file_queue) -> None:
        self.__file_queue = file_queue

    @property
    def file_repo(self) -> str:
        return self.__file_repo

    @file_repo.setter
    def file_repo(self, file_repo) -> None:
        self.__file_repo = file_repo

    @property
    def jano_enabled(self) -> bool:
        return self.__jano_enabled

    @jano_enabled.setter
    def jano_enabled(self, jano_enabled) -> None:
        self.__jano_enabled = jano_enabled

    # @property
    # def scopesDeAplicacion(self):
    #     return self.__scopesDeAplicacion

    # @scopesDeAplicacion.setter
    # def scopesDeAplicacion(self, scopesDeAplicacion):
    #     self.__scopesDeAplicacion = scopesDeAplicacion

    # @property
    # def audiences(self):
    #     return self.__audiences

    # @audiences.setter
    # def audiences(self, audiences):
    #     self.__audiences = audiences
