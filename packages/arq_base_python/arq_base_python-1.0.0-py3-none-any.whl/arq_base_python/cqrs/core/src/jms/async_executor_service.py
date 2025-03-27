import asyncio
import uuid
import time
import logging
import reactivex
from reactivex import operators as op
from reactivex import Observable

from cqrs.core.src.jms.tipo_ejecutable import TipoEjecutable
from cqrs.core.src.handlers.handler_resolver import HandlerResolver
from cqrs.core.src.model.exec_dto import ExecDTO
from cqrs.core_api.src.event.event_result import EventResult
from cqrs.core_api.src.jms.core_message_publisher import CoreMessagePublisher
from cqrs.core_api.src.messaging.message_serializer import MessageSerializer
from cqrs.core_api.src.models.aplicacion_emisora import AplicacionEmisora
from cqrs.core_api.src.models.aplicacion_origen import AplicacionOrigen
from cqrs.core_api.src.models.common_body import CommonBody
from cqrs.core_api.src.models.event import Event
from cqrs.core_api.src.models.event_submitted import EventSubmitted
from jano.core.src.secured_application import SecuredApplication


class AsyncExecutorService:
    def __init__(
            self,
            serializer: MessageSerializer,
            secured_application: SecuredApplication,
            send_message_to_mq: CoreMessagePublisher,
            handler_resolver: HandlerResolver
    ):
        self.log = logging.getLogger(__name__)
        self.serializer = serializer
        self.secured_application = secured_application
        self.send_message_to_mq = send_message_to_mq
        self.handler_resolver = handler_resolver

    def execute(self, tipo: TipoEjecutable, body: str) -> Observable:
        return reactivex.just(body).pipe(
            op.map(lambda x: self.convertir_a_dto(tipo, x)),
            op.filter(lambda x: self.__check_for_no_ui_event(x)),
            op.flat_map(lambda x: self.__flat_map(x)),
            # op.catch(lambda ex, _: self.log.error(
            #     f"Error en el flujo CATCH: {ex}")),
        )

    def __flat_map(self, dto: ExecDTO):
        handler = self.__find_handler(exec_dto=dto)
        if handler:
            try:
                return self.__publicar_eventos(self.execute_with_handler(
                    dto, handler), dto)
            except Exception as t:
                self.log.error(
                    f"Se detecto un error y se detendra la ejecucion del Flux: {str(t)}")
                raise t
        else:
            self.log.error(
                f"No se encontro un handler para el evento {dto.submitted.get().nombre}")
            return reactivex.empty()

    def __publicar_eventos(self, event: Observable[Event], async_dto: ExecDTO):
        return event.pipe(
            op.map(lambda event: self.__decorar_resultado(
                async_dto=async_dto, event=event)),
            op.flat_map(
                lambda event_submitted: self.__publicar_evento(event_submitted))
        )

    def __publicar_evento(self, event_submitted: EventSubmitted):
        event = event_submitted.get()
        if event_submitted.get_validation_status() != 0:
            self.send_message_to_mq.publishError(
                event, event_submitted.get_validation_message())
        else:
            asyncio.create_task(self.send_message_to_mq.publish(event))
        return reactivex.just(event)

    def __decorar_resultado(self, async_dto: ExecDTO, event: Event):
        self.log.debug(f"Evento recibido del ejecutor {event}")
        if not event.id or event.id.lower().strip() == "":
            event.id = str(uuid.uuid4())

        event.aplicacion_origen = event.aplicacion_origen if event.aplicacion_origen else AplicacionOrigen(
            str(self.secured_application.id_app_proteccion), self.secured_application.name)

        if async_dto.tipo == TipoEjecutable.COMANDO:
            event.usuario = async_dto.submitted.get().usuario
            event.dni = async_dto.submitted.get().dni
            event.aplicacion_origen = async_dto.submitted.get().aplicacion_origen if async_dto.submitted.get(
            ).aplicacion_origen else AplicacionOrigen(str(self.secured_application.id_app_proteccion), self.secured_application.name)
        else:
            async_dto.submitted.get().usuario.ip = ""
            event.usuario = async_dto.submitted.get().usuario
            event.dni = async_dto.submitted.get().dni
            event.aplicacion_origen = async_dto.submitted.get().aplicacion_origen if async_dto.submitted.get(
            ).aplicacion_origen else AplicacionOrigen(str(self.secured_application.id_app_proteccion), self.secured_application.name)

        if event.aplicacion_emisora is None:
            event.aplicacion_emisora = AplicacionEmisora()

        event.aplicacion_emisora.id_aplicacion_emisora = self.secured_application.id_app_proteccion
        event.aplicacion_emisora.nombre_aplicacion_emisora = self.secured_application.name

        if async_dto.tipo == TipoEjecutable.COMANDO:
            event.idComando = async_dto.submitted.get().id
        else:
            event.idComando = async_dto.submitted.get().idComando

        event.timestamp = time.time()
        if not event.resultado or event.resultado.lower().strip() == "":
            event.resultado = EventResult.EXITO.name

        self.log.debug(f"Evento decorado {event}")
        return EventSubmitted(event)

    def execute_with_handler(self, exec_dto: ExecDTO, handler) -> Observable:
        self.log.debug(
            f"Execute with automatic parser (New API) {exec_dto.submitted.get().nombre}")
        payload = self.serializer.parse_payload(
            exec_dto.submitted.get().payload, handler.get_input_class())
        common_body: CommonBody = exec_dto.submitted.get()
        common_body.payload = payload
        return handler.get_handler()(common_body)

    def __find_handler(self, exec_dto: ExecDTO):
        message_name = exec_dto.submitted.get().nombre
        return self.handler_resolver.get_event_listener(message_name) if exec_dto.is_event() else self.handler_resolver.get_command_handler(message_name)

    def __check_for_no_ui_event(self, dto: ExecDTO):
        if dto.is_ui_event():
            self.log.debug(
                f"Evento {dto.submitted.get().nombre} es del tipo UI y no es ejecutable.")
        return not dto.is_ui_event()

    def convertir_a_dto(self, tipo: TipoEjecutable, cuerpo: str):
        self.log.debug("Convirtiendo en DTO")
        dto = ExecDTO()
        dto.tipo = tipo
        if tipo == TipoEjecutable.COMANDO:
            dto.submitted = self.serializer.to_command_submitted(cuerpo)
        else:
            dto.submitted = self.serializer.to_event_submitted(cuerpo)
        return dto
