import asyncio
import logging
from reactivex import Observable, of, operators as op
from fastapi.responses import JSONResponse

from cqrs.core_api.src.models.command_submitted import (
    CommandSubmitted,
)
from cqrs.core_api.src.models.command_error import CommandError
from cqrs.core_api.src.models.command_ack import CommandAck
from cqrs.core_api.src.command.security_helper import (
    SecurityHelper,
)
from cqrs.core.src.jms.message_publisher import MessagePublisher
from cqrs.core_api.src.messaging.reactive_message_publisher import (
    ReactiveMessagePublisher,
)
from jano.core.src.secured_application import SecuredApplication


class CommandService:
    def __init__(
        self,
        message_publisher: ReactiveMessagePublisher,
        secured_application: SecuredApplication,
        security_helper: SecurityHelper,
    ):
        self.log = logging.getLogger(__name__)
        self.secured_application = secured_application
        self.security_helper = security_helper
        self.message_publisher = message_publisher

    async def process_command(self, command: CommandSubmitted, request) -> JSONResponse:
        command_sub_enrich = self.security_helper.enrich_with_security_props(
            command, request
        )

        published_message = await self._publish(command_sub_enrich)

        if published_message:
            self.log.debug("Mensaje publicado a bus de eventos de spring")

        return self.receive_build_response(observer_object=of(command))

    def receive_build_response(self, observer_object) -> JSONResponse:
        observer_object = observer_object.pipe(
            op.map(self._build_response)
        )
        return observer_object.run()

    def receive_command_sub_enrich(self, observer_object):
        observer_object = observer_object.pipe(
            op.map(self._publish)
        )
        return observer_object.run()

    def print_command_service(self, command: CommandSubmitted):
        self.log.debug("Procesando comando...")
        self.log.debug(f"Comando recibido: {command}")
        self.security_helper.enrich_with_security_props(command, [])

    async def _publish(self, commandSub: CommandSubmitted):
        if commandSub.get_validation_status() != 0:
            return False
        asyncio.create_task(self.message_publisher.publish(commandSub))
        return True

    def _build_response(self, command: CommandSubmitted) -> JSONResponse:
        if command.get_validation_status() == 0:
            self.log.debug("Devolviendo respuesta 202")
            return JSONResponse(content=self._create_ack(command), status_code=202)
        else:
            self.log.debug("Devolviendo respuesta 422")
            response = {
                CommandError.codigo: command.get_validation_status(),
                CommandError.mensaje: command.get_validation_message(),
            }
            return JSONResponse(content=response, status_code=422)

    def _create_ack(self, command: CommandSubmitted) -> CommandAck:
        self.log.debug(
            "Creando objeto ACK para la peticion de procesar Command")
        ack_obj = CommandAck(
            command.get().id,
            command.get().nombre,
            command.get().id_trazabilidad,
            self.secured_application.id_app_proteccion,
            command.get().usuario.nombre,
            command.get().usuario.id_session,
            command.get().timestamp,
        )
        self.log.debug(f"{ack_obj}")
        return ack_obj.build_response()
