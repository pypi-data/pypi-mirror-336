from arq_base_python.cqrs.core_api.src.messaging.reactive_message_publisher import (
    ReactiveMessagePublisher,
)
from arq_base_python.cqrs.core_api.src.models.event import Event
from arq_base_python.cqrs.core_api.src.models.submittable import Submittable
from arq_base_python.cqrs.core_api.src.jms.core_message_publisher import (
    CoreMessagePublisher,
)
import logging


class MessagePublisher(ReactiveMessagePublisher):

    def __init__(self, send_message_to_mq: CoreMessagePublisher):
        self.send_message_to_mq = send_message_to_mq
        self.log = logging.getLogger(__name__)
        # self.serializer = serializer

    async def publish(self, var1: Submittable):
        if self._submittable_has_content(var1):
            await self.send_message_to_mq.publish(var1.get())
        else:
            self.log.error("No se puede publicar un comando o evento nulo")

    def publish_for_log(self, var1: Submittable) -> str:
        return super().publish_for_log(var1)

    def _submittable_has_content(self, submittable: Submittable) -> bool:
        if (
            submittable is not None
            and submittable.get()
            and submittable.get_validation_status() == 0
        ):
            return True
        return False

    def initialize_event_properties(self, var1: Event, var2: Submittable) -> str:
        return super().initialize_event_properties(var1, var2)
