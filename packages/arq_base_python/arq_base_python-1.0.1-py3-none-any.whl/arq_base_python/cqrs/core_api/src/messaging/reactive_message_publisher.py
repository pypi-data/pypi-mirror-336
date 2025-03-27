import abc

from arq_base_python.cqrs.core_api.src.messaging.i_message_publisher import (
    IMessagePublisher,
)


class ReactiveMessagePublisher(IMessagePublisher, abc.ABC):
    pass
