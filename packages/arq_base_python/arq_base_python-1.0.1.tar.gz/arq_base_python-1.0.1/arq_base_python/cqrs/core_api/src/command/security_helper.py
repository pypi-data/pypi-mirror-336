import abc
from dataclasses import dataclass, field

from arq_base_python.cqrs.core_api.src.models.command_submitted import (
    CommandSubmitted,
)


class SecurityHelper(abc.ABC):
    @abc.abstractmethod
    def enrich_with_security_props(
        self, var1: CommandSubmitted, var2: object
    ) -> CommandSubmitted:
        pass

    # @abc.abstractmethod
    # def print_application_data(self) -> dict:
    #     pass

    # @abc.abstractmethod
    # def get_secured_application(self) -> object:
    #     pass
