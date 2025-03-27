import asyncio
import logging

import reactivex
from reactivex import of, operators as op

from arq_base_python.cqrs.core.src.jms.tipo_ejecutable import TipoEjecutable
from arq_base_python.cqrs.core.src.jms.send_message_to_mq import SendMessageToMQ
from arq_base_python.cqrs.core_api.src.jms.base_message import BaseMessage
from arq_base_python.cqrs.core_api.src.jms.i_receive_message_from_source import IReceiveMessageFromSource
from arq_base_python.cqrs.core_api.src.models.received_message import ReceivedMessage
from arq_base_python.cqrs.core.src.jms.async_executor_service import AsyncExecutorService


class ReceiveMessageFromSource(IReceiveMessageFromSource):

    def __init__(self, send_message_to_mq: SendMessageToMQ, async_executor_service: AsyncExecutorService):
        self.log = logging.getLogger(__name__)
        self.send_message_to_mq = send_message_to_mq
        self.async_executor_service = async_executor_service

    def processMessage(self, var1: BaseMessage):
        base_message = of(var1)
        base_message.pipe(
            op.flat_map(
                lambda base_message: self.receive_base_message(base_message)),
        ).subscribe()

    def _handle_error_obs(self, base_message: BaseMessage, e):
        self.log.error(f"Se capturo una excepcion en el Flux: {str(e)}")
        self.log.warning("El mensaje se llevara al destino MQ de Errores")
        asyncio.create_task(self.send_message_to_mq.publishError(
            message=base_message.get_body(), errorMSG=str(e)))

    def _execute_filtered_message(self, received_message: ReceivedMessage):
        if received_message.type.lower() != "COMMAND".lower():
            tipo = TipoEjecutable.EVENTO
        else:
            tipo = TipoEjecutable.COMANDO

        return self.async_executor_service.execute(
            tipo=tipo, body=received_message.content)

    def receive_base_message(self, var1: BaseMessage):
        source = of(var1)
        observable = source.pipe(
            op.map(self.parse),
            op.filter(self.filter_base_message),
            op.flat_map(self._execute_filtered_message),
        )
        observable.subscribe(
            on_next=lambda v: self.log.debug(
                f"Mensaje {var1.__hash__()} procesado"),
            on_error=lambda e: self._handle_error_obs(var1, e),
        )
        return reactivex.empty()

    def parse(self, mqMessage: BaseMessage):
        try:
            contents = mqMessage.get_body()
            msgType = mqMessage.get_headers().get("type", "TYPE-DESCONOCIDO")
            jmsID = mqMessage.get_message_id(
            ) if mqMessage.get_message_id() else "JMSMessageID-Desconocido"
            return ReceivedMessage(type=msgType, content=contents, jmsID=jmsID)
        except Exception as e:
            self.log.error(
                f"Error parseando en mensaje recibido de MQ: {str(e)}")
            return None

    def filter_base_message(self, received_message: ReceivedMessage):
        if received_message.type.lower() != "COMMAND".lower() and received_message.type.lower() != "EVENT".lower():
            if received_message.type.lower() == "LOG".lower():
                return False
            else:
                self.log.error(
                    "Mensaje recibido no esta tipificado COMMAND o EVENT.")
                asyncio.create_task(self.send_message_to_mq.publishError(
                    message=received_message.content, errorMSG="Mensaje recibido no esta tipificado COMMAND o EVENT."))
                return False
        else:
            return True
