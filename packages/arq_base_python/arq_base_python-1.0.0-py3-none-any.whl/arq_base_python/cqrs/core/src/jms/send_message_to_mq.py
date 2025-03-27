import json
import logging
import functools
from datetime import date
from typing import Tuple
from collections import deque
import uuid

from cqrs.core_api.src.event.event_error import EventError
from cqrs.core_api.src.jms.core_message_publisher import (
    CoreMessagePublisher,
)
from cqrs.core_api.src.models.command_submitted import (
    CommandSubmitted,
)
from cqrs.core_api.src.models.event_submitted import (
    EventSubmitted,
)
from cqrs.core_api.src.models.command import Command
from cqrs.core_api.src.models.event import Event
from cqrs.core_api.src.models.common_body import CommonBody
from cqrs.core_api.src.models.submittable import Submittable
from cqrs.core_api.src.properties.destinations import (
    Destinations,
)
from cqrs.core_api.src.jms.concrete_sender import ConcreteSender
from cqrs.core_api.src.messaging.message_serializer import (
    MessageSerializer,
)
from cqrs.core.src.jms.message_properties import (
    MessageProperties,
)
from cqrs.core.src.jms.properties_creator import (
    PropertiesCreator,
)
from cqrs.core_api.src.jms.base_message import BaseMessage
from helpers.filequeue_fallback.src.file_queue_fallback import FileQueueFallBack


class SendMessageToMQ(CoreMessagePublisher):

    def __init__(
        self,
        properties_creator: PropertiesCreator,
        mq_destinations: Destinations,
        sender: ConcreteSender,
        serializer: MessageSerializer,
    ) -> None:
        self.log = logging.getLogger(__name__)
        self.properties_creator = properties_creator
        self.mq_destinations = mq_destinations
        self.sender = sender
        self.serializer = serializer

    def __parse_to_event_error(self, input):
        if not input:
            raise Exception("El objeto a convertir es nulo")
        else:
            event_error = EventError()
            if isinstance(input, CommandSubmitted):
                event_error = self.__parse_to_event_error_from_command(
                    commandSubmitted=input)
            else:
                if not isinstance(input, EventSubmitted):
                    if isinstance(input, EventError):
                        return event_error
                    else:
                        raise Exception(
                            "El objeto a convertir no es ni comando ni evento")
                event_error = self.__parse_to_event_error_from_event(
                    event_submitted=input)
            return event_error

    def __parse_to_event_error_from_command(self, commandSubmitted):
        if not commandSubmitted.get():
            raise Exception("El objeto no tiene un comando valido o es nulo.")
        else:
            event_error = EventError()
            event_error.uuid = commandSubmitted.get().id
            event_error.name = commandSubmitted.get().nombre
            event_error.json = self.serializer.serialize(
                var1=commandSubmitted.__dict__())
            event_error.fechaEvento = date.today().strftime('%Y-%m-%d')
            event_error.clase = "COMANDO"
            if commandSubmitted.get().dni is not None:
                event_error.dni = commandSubmitted.get().dni.identificacion
                event_error.tipoDni = commandSubmitted.get().dni.tipo_identificacion
            return event_error

    def __parse_to_event_error_from_event(self, event_submitted):
        if not event_submitted.get():
            raise Exception("El objeto no tiene un evento valido o es nulo.")
        else:
            event_error = EventError()
            event_error.name = event_submitted.get().nombre
            event_error.uuid = event_submitted.get().id
            event_error.json = self.serializer.serialize(
                var1=event_submitted.__dict__())
            event_error.clase = "EVENTO"
            event_error.fechaEvento = date.today().strftime('%Y-%m-%d')
            if event_submitted.get().dni is not None:
                event_error.tipoDni = event_submitted.get().dni.tipo_identificacion
                event_error.dni = event_submitted.get().dni.identificacion
            return event_error

    def _extract_msg_data(
        self, pubmsg: CommonBody
    ) -> Tuple[str, str, Submittable, MessageProperties]:
        if pubmsg is None:
            raise Exception("No se puede publicar un comando/evento Nulo")
        else:
            submittable = self._parse_to_submittable(pubmsg)
            type_ = ""
            jsonMessage = ""
            properties = MessageProperties()
            if isinstance(pubmsg, Event):
                type_ = "Evento"
                app_origen = pubmsg.aplicacion_origen.id_aplicacion_origen if pubmsg.aplicacion_origen else ""
                properties = self.properties_creator.for_event(
                    pubmsg.eventScope, app_origen, pubmsg.nombre
                )
            elif isinstance(pubmsg, Command):
                type_ = "Comando"
                properties = self.properties_creator.for_command()
            jsonMessage = self.serializer.serialize_submittable(submittable)
            return (type_, jsonMessage, submittable, properties)

    def _parse_to_submittable(self, pubmsg: CommonBody) -> Submittable:
        if isinstance(pubmsg, Event):
            return EventSubmitted(pubmsg)
        elif isinstance(pubmsg, Command):
            return CommandSubmitted(pubmsg)
        else:
            raise ValueError("Invalid pubmsg type")

    def _get_serialized_message(self, message):
        return message if isinstance(message, str) else self.serializer.serialize(
            var1=message
        )

    def _execute_retry_with_fallback(func_fallback):
        @functools.wraps(func_fallback)
        def receive_function(func):
            @functools.wraps(func)
            def wrapper_function(*args, **kwargs):
                for _ in range(1, 6):
                    try:
                        self = args[0]
                        # self.log.debug(
                        #     f"Iniciando intento de publicacion {i} de 5")
                        r = func(*args, **kwargs)
                    except Exception as error:
                        self.log.debug(
                            f"Mensaje no se pudo publicar, llamando CallBack de Almacenamiento ({args[1].nombre}-{'HASHCODE'})")
                        func_fallback(
                            self=self,
                            objToSubmit=self._parse_to_submittable(args[1]),
                            destino=self.mq_destinations.get_publish_destination(),
                            errorCode=str(error)
                        )
                    else:
                        return r

            return wrapper_function

        return receive_function

    def __persists_with_fallback_reactive(self, objToSubmit, destino, errorCode):
        event_error = self.__parse_to_event_error(input=objToSubmit)
        event_error.errorDescription = f"destino: {destino}, error: {errorCode}"
        file_queue_fallback = FileQueueFallBack(persistentFsQueue=deque())
        file_queue_fallback.add(var1=event_error)
        self.log.debug(
            f"Garantia de entrega: Objeto no publicado fue almacenado en mecanismo de fallback ({objToSubmit})")

    def _extract_id(self, json_string):
        try:
            json_dict = json.loads(json_string)
            if "comando" in json_dict:
                return json_dict["comando"]["id"]
            elif "evento" in json_dict:
                return json_dict["evento"]["id"]
        except Exception as e:
            return str(uuid.uuid4())

    @_execute_retry_with_fallback(__persists_with_fallback_reactive)
    async def publish(self, pubmsg: CommonBody):
        type_, jsonMessage, submittable, properties = self._extract_msg_data(
            pubmsg)
        properties.add("id", pubmsg.id)

        self.log.debug(
            f"Publicando {type_} ({pubmsg.nombre}-{pubmsg.__hash__()})")
        message = BaseMessage(
            jsonMessage, properties.get_properties())
        await self.sender.send(
            self.mq_destinations.get_publish_destination(), message)
        self.log.debug(
            f"{type_} Publicado  ({pubmsg.nombre}-{pubmsg.__hash__()})")

    @_execute_retry_with_fallback(__persists_with_fallback_reactive)
    async def publishError(self, message, errorMSG):
        self.log.info(
            f"Publicando mensaje ({message}) a topico con log Error, mensaje: ({errorMSG})")

        error_headers = {
            "id": self._extract_id(message),
            "type": "LOG",
        }
        msg = BaseMessage(
            body=self._get_serialized_message(message),
            headers=error_headers,
            error=errorMSG
        )
        await self.sender.send_error(self.mq_destinations.get_publish_destination(), msg)
        self.log.info(
            f"Publicado mensaje de error ({errorMSG})")
