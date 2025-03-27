from dataclasses import dataclass, field
from typing_extensions import Annotated
from dataclass_wizard import property_wizard


@dataclass(init=False)
class ReceivedMessage(metaclass=property_wizard):

    type: Annotated[str, field(default="")]
    content: Annotated[str, field(default="")]
    jmsID: Annotated[str, field(default="")]

    __type: str = field(repr=False, init=False)
    __content: str = field(repr=False, init=False)
    __jmsID: str = field(repr=False, init=False)

    def __init__(
        self,
        type: str = None,
        content: str = None,
        jmsID: str = None,
    ):
        self.__type = type
        self.__content = content
        self.__jmsID = jmsID


    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, type: str):
        self.__type = str(type)

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, content: str):
        self.__content = str(content)

    @property
    def jmsID(self) -> str:
        return self.__jmsID

    @jmsID.setter
    def jmsID(self, jmsID: str):
        self.__content = str(jmsID)
