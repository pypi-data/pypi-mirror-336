import abc

from cqrs.core_api.src.messaging.i_message_publisher import (
    IMessagePublisher,
)


class ReactiveMessagePublisher(IMessagePublisher, abc.ABC):
    pass
