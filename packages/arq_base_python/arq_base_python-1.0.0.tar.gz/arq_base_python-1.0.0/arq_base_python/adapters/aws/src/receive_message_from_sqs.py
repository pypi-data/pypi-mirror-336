import uuid
from adapters.aws.src.aws_sqs_listener import SqsListener
from cqrs.core_api.src.jms.i_receive_message_from_source import IReceiveMessageFromSource
from cqrs.core_api.src.jms.base_message import BaseMessage


class ReceiveMessageFromSQS(SqsListener):
    def __init__(self, i_receive_message_from_source: IReceiveMessageFromSource, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._receive_message_from_source = i_receive_message_from_source

    def handle_message(self, body, messages_attributes):
        self._receive_message_from_source.processMessage(
            self.to_base_message(body, self.parse_headers(messages_attributes)))

    def parse_headers(self, headers):
        return headers if headers else {}

    def to_base_message(self, body, headers) -> BaseMessage[str]:
        message = BaseMessage(body, headers)
        message.set_message_id(str(uuid.uuid4()))
        return message
