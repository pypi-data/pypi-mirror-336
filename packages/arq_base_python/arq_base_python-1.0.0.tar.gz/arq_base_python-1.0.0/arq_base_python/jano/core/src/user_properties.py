from dataclasses import dataclass, field
from typing_extensions import Annotated
from dataclass_wizard import property_wizard

from jano.core.src.identity.identificacion import Identificacion


@dataclass(init=False)
class UserProperties(metaclass=property_wizard):

    # DEFAULT_NIVEL_SEGURIDAD: Annotated[int, field(default=5)]

    subject: Annotated[str, field(default="")]
    displayName: Annotated[str, field(default="")]
    givenName: Annotated[str, field(default="")]
    surName: Annotated[str, field(default="")]
    email: Annotated[str, field(default="")]
    identificacion: Annotated[dict, field(default={})]
    roles: Annotated[list, field(default=[])]
    groups: Annotated[list, field(default=[])]
    nivelSeguridad: Annotated[int, field(default=5)]
    realm: Annotated[str, field(default="")]
    userType: Annotated[str, field(default="")]
    ipAddress: Annotated[str, field(default="")]
    uuidSession: Annotated[str, field(default="")]
    accountEnabled: Annotated[bool, field(default="")]
    objectId: Annotated[str, field(default="")]

    __subject: str = field(repr=False, init=False)
    __displayName: str = field(repr=False, init=False)
    __givenName: str = field(repr=False, init=False)
    __surName: str = field(repr=False, init=False)
    __email: str = field(repr=False, init=False)
    __identificacion: dict = field(repr=False, init=False)
    __roles: list = field(repr=False, init=False)
    __groups: list = field(repr=False, init=False)
    __nivelSeguridad: int = field(repr=False, init=False)
    __realm: str = field(repr=False, init=False)
    __userType: str = field(repr=False, init=False)
    __ipAddress: str = field(repr=False, init=False)
    __uuidSession: str = field(repr=False, init=False)
    __accountEnabled: bool = field(repr=False, init=False)
    __objectId: str = field(repr=False, init=False)

    def __init__(
        self,
        subject: str = None,
        displayName: str = None,
        givenName: str = None,
        surName: str = None,
        email: str = None,
        identificacion: dict = {},
        roles: list = None,
        groups: list = None,
        nivelSeguridad: int = 5,
        realm: str = None,
        userType: str = None,
        ipAddress: str = None,
        uuidSession: str = None,
        accountEnabled: bool = False,
        objectId: str = None,
    ):
        self.__subject = subject
        self.__displayName = displayName
        self.__givenName = givenName
        self.__surName = surName
        self.__email = email
        self.__identificacion = Identificacion(**identificacion)
        self.__roles = roles if roles is not None else []
        self.__groups = groups if groups is not None else []
        self.__nivelSeguridad = nivelSeguridad
        self.__realm = realm
        self.__userType = userType
        self.__ipAddress = ipAddress
        self.__uuidSession = uuidSession
        self.__accountEnabled = accountEnabled
        self.__objectId = objectId

    @property
    def subject(self) -> str:
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = str(subject)

    @property
    def displayName(self) -> str:
        return self.__displayName

    @displayName.setter
    def displayName(self, displayName):
        self.__displayName = str(displayName)

    @property
    def givenName(self) -> str:
        return self.__givenName

    @givenName.setter
    def givenName(self, givenName):
        self.__givenName = givenName

    @property
    def surName(self) -> str:
        return self.__surName

    @surName.setter
    def surName(self, surName):
        self.__surName = str(surName)

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, identificacion):
        self.__identificacion = identificacion

    @property
    def roles(self) -> list:
        return self.__roles

    @roles.setter
    def roles(self, roles):
        self.__roles = roles

    @property
    def groups(self) -> list:
        return self.__groups

    @groups.setter
    def groups(self, groups):
        self.__groups = groups

    @property
    def nivelSeguridad(self) -> int:
        return self.__nivelSeguridad

    @nivelSeguridad.setter
    def nivelSeguridad(self, nivelSeguridad):
        self.__nivelSeguridad = nivelSeguridad

    @property
    def realm(self) -> str:
        return self.__realm

    @realm.setter
    def realm(self, realm):
        self.__realm = realm

    @property
    def userType(self) -> str:
        return self.__userType

    @userType.setter
    def userType(self, userType):
        self.__userType = userType

    @property
    def ipAddress(self) -> str:
        return self.__ipAddress

    @ipAddress.setter
    def ipAddress(self, ipAddress):
        self.__ipAddress = ipAddress

    @property
    def uuidSession(self) -> str:
        return self.__uuidSession

    @uuidSession.setter
    def uuidSession(self, uuidSession):
        self.__uuidSession = uuidSession

    @property
    def accountEnabled(self) -> bool:
        return self.__accountEnabled

    @accountEnabled.setter
    def accountEnabled(self, accountEnabled):
        self.__accountEnabled = accountEnabled

    @property
    def objectId(self) -> str:
        return self.__objectId

    @objectId.setter
    def objectId(self, objectId):
        self.__objectId = objectId
