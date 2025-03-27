import logging

from dependency_injector.wiring import Provide, inject
from reactivex import of
from reactivex import operators as op
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from cqrs.core_api.src.models.command import Command
from cqrs.core_api.src.models.command_error import CommandError
from cqrs.core_api.src.models.command_submitted import (
    CommandSubmitted,
)


from entrypoints_base.command_receiver.src.commands.web.command_body_validator import (
    CommandBodyValidator,
)
from entrypoints_base.command_receiver.src.commands.web.command_authorizer import (
    CommandAuthorizer,
)
from entrypoints_base.command_receiver.src.commands.web.command_service import (
    CommandService,
)


from containers.application_container import Application


COMMAND_FIELD = "comando"
NO_COMMAND_IN_REQUEST = {}
AUTORIZATION_END_MSG = "Fin Autorizacion [Etapa_2] = %s"


class CommandHandler:

    @inject
    def __init__(
        self,
        command_body_validator: CommandBodyValidator = Provide[
            Application.command_handler_container.command_validator_container.command_validator
        ],
        command_authorizer: CommandAuthorizer = Provide[
            Application.command_handler_container.command_authorizer_container.command_authorizer
        ],
        command_service: CommandService = Provide[
            Application.command_handler_container.command_service_container.command_service
        ],
    ) -> None:
        self.command_body_validator = command_body_validator
        self.command_authorizer = command_authorizer
        self.command_service = command_service
        self.log = logging.getLogger(__name__)

    async def receive_command(self, request: Request, data) -> JSONResponse:
        self.log.debug(
            "Inicia Autorizacion [Etapa_2] (validar estructura, nombre de comando y permiso para invocarlo)..."
        )
        try:
            command_data: dict = data.get(COMMAND_FIELD, None)
            if command_data:
                command_submitted = of(CommandSubmitted(
                    comando=Command(**command_data)))
            else:
                command_submitted = of(CommandSubmitted())
        except Exception as e:
            self.log.error("Error al recibir el comando: %s", e)
            command_submitted = of(CommandSubmitted(comando=Command({})))
        else:
            pass
        finally:
            pass

        command_submitted.run()

        var10001 = self.command_body_validator

        cs_performed_subscriber = var10001.perform_validation(
            command=command_submitted)

        list_ = []

        cs_performed_subscriber.subscribe(
            on_next=lambda l: list_.append(l),
            on_error=lambda e: self.log.error(
                f"Perform validation error: {e}"),
        )

        cs_performed = list_[0]

        if cs_performed.get_validation_status() != 0:
            self.log.debug(
                AUTORIZATION_END_MSG, "NO-AUTORIZADO-400-BAD-REQUEST"
            )
            response = {
                CommandError.codigo: str(cs_performed.get_validation_status()),
                CommandError.comando: self._get_nombre_comando(cs_performed),
                CommandError.mensaje: cs_performed.get_validation_message(),
            }
            return JSONResponse(content=response, status_code=cs_performed.get_validation_status())
        else:
            result = self.command_authorizer.authorize_recieve_command(
                cs_performed, request
            )
            if result:
                self.log.debug(AUTORIZATION_END_MSG, "AUTORIZADO")
                return await self.command_service.process_command(cs_performed, request)
            else:
                self.log.debug(
                    AUTORIZATION_END_MSG, "NO-AUTORIZADO")
                response = {
                    CommandError.codigo: "403",
                    CommandError.comando: self._get_nombre_comando(cs_performed),
                    CommandError.mensaje: "No tiene autorizacion para invocar el comando",
                }
                return JSONResponse(content=response, status_code=403)

    def _get_nombre_comando(self, command: CommandSubmitted) -> str:
        if command == None:
            return "-vacio-"
        else:
            if command.get() == None:
                return "-vacio-"
            else:
                return command.get().nombre
