from dataclass_wizard import property_wizard
from typing_extensions import Annotated
from dataclasses import dataclass, field

from arq_base_python.cqrs.core.src.jms.tipo_ejecutable import TipoEjecutable
from arq_base_python.cqrs.core_api.src.event.event_scope import EventScope
from arq_base_python.cqrs.core_api.src.models.submittable import Submittable
from arq_base_python.cqrs.core_api.src.models.base_executor import BaseExecutor
from arq_base_python.cqrs.core_api.src.models.base_serializable import BaseSerializable


@dataclass(init=False)
class ExecDTO(metaclass=property_wizard):
    tipo: Annotated[TipoEjecutable, field(default=None)]
    submitted: Annotated[Submittable, field(default=None)]
    executor: Annotated[BaseExecutor, field(default=None)]
    depend: Annotated[dict, field(default={})]
    serializable: Annotated[BaseSerializable, field(default=None)]

    __tipo: str = field(repr=False, init=False)
    __submitted: str = field(repr=False, init=False)
    __executor: str = field(repr=False, init=False)
    __depend: dict = field(repr=False, init=False)
    __serializable: str = field(repr=False, init=False)

    def __init__(
        self,
        tipo: TipoEjecutable = None,
        submitted: Submittable = None,
        executor: BaseExecutor = None,
        depend: dict = None,
        serializable: BaseSerializable = None
    ):
        self.__tipo = tipo
        self.__submitted = submitted
        self.__executor = executor
        self.__depend = depend
        self.__serializable = serializable

    @property
    def tipo(self) -> TipoEjecutable:
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        self.__tipo = tipo

    @property
    def submitted(self) -> Submittable:
        return self.__submitted

    @submitted.setter
    def submitted(self, submitted):
        self.__submitted = submitted

    @property
    def executor(self) -> BaseExecutor:
        return self.__executor

    @executor.setter
    def executor(self, executor):
        self.__executor = executor

    @property
    def depend(self) -> dict:
        return self.__depend

    @depend.setter
    def depend(self, depend):
        self.__depend = depend

    @property
    def serializable(self) -> BaseSerializable:
        return self.__serializable

    @serializable.setter
    def serializable(self, serializable):
        self.__serializable = serializable

    def is_event(self):
        return self.tipo == TipoEjecutable.EVENTO

    def __validate_is_ui_event(self, event_submitted):
        return EventScope.SCOPE_UI.get_scope() == event_submitted.get().eventScope

    def is_ui_event(self) -> bool:
        return self.is_event() and self.submitted != None and self.__validate_is_ui_event(event_submitted=self.submitted)
