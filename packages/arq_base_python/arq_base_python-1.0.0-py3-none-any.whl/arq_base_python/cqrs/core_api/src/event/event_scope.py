from enum import Enum


class EventScope(Enum):
    SCOPE_UI = "SEND_TO_UI"
    SCOPE_MQ = "SEND_TO_MQ"
    SCOPE_ALL = "SEND_TO_ALL"
    SCOPE_EXT = "SEND_TO_EXT"

    def __init__(self, scope):
        self.__scope = scope

    def get_scope(self) -> str:
        return self.__scope

    @classmethod
    def get(cls, scope):
        for member in cls:
            if member.get_scope() == scope:
                return member
        return cls.SCOPE_MQ
