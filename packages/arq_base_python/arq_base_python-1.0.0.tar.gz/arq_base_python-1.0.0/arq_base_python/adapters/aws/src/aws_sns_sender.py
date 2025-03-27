from aioboto3.session import Session as AsyncSession
from cqrs.core_api.src.jms.concrete_sender import ConcreteSender
from cqrs.core_api.src.jms.base_message import BaseMessage
from typing import TypeVar
import logging
from botocore.exceptions import ClientError
from boto3 import Session
import uuid
from datetime import datetime


T = TypeVar("T")


class MessageHeaders:
    def __init__(self, headers: dict = {}):
        self.headers = {
            "timestamp": str(datetime.now().isoformat()),
        }
        if headers:
            self.headers.update(headers)

    def get_headers(self):
        return self.headers

    def update_headers(self, headers: dict):
        if not isinstance(headers, dict):
            raise ValueError("El valor proporcionado debe ser un diccionario")
        self.headers.update(headers)


class AwsSnsSender(ConcreteSender):

    def __init__(self, aws_session: Session, async_session: AsyncSession):
        self.sns_resource = aws_session.resource("sns")
        self.sts_client = aws_session.client("sts")
        self.topic = None
        self.async_session = async_session
        self.log = logging.getLogger(__name__)

    async def send(self, destination: str, base_message: BaseMessage[T]):
        self.topic = self._get_topic(destination)
        message_headers = MessageHeaders(base_message.get_headers())
        await self.publish_message(base_message.get_body(),
                                   message_headers.get_headers())

    async def send_error(self, destination: str, base_message: BaseMessage[T]):
        self.topic = self._get_topic(destination)
        message_headers = MessageHeaders(base_message.get_headers())
        await self.publish_message(str(base_message),
                                   message_headers.get_headers())

    async def publish_message(self, message, attributes):
        """
        Publishes a message, with attributes, to a topic. Subscriptions can be filtered
        based on message attributes so that a subscription receives messages only
        when specified attributes are present.

        :param topic: The topic to publish to.
        :param message: The message to publish.
        :param attributes: The key-value attributes to attach to the message. Values
                           must be either `str` or `bytes`.
        :return: The ID of the message.
        """
        try:
            att_dict = self._create_message_attributes(attributes)
            async with self.async_session.client('sns', ) as sns_client:
                response = await sns_client.publish(
                    TopicArn=self.topic,
                    Message=message,
                    MessageAttributes=att_dict
                )
                message_id = response["MessageId"]
        except ClientError:
            self.log.exception(
                "Ocurrio un error al publicar un mensaje al tópico(%s.)", self.topic)
            raise
        else:
            return message_id

    def _create_message_attributes(self, attributes):
        """
        Creates a message attributes dictionary.

        :param attributes: The key-value attributes to attach to the message. Values
                           must be either `str` or `bytes`.
        :return: The message attributes dictionary.
        """
        att_dict = {}
        for key, value in attributes.items():
            if isinstance(value, str):
                att_dict[key] = {"DataType": "String", "StringValue": value}
            elif isinstance(value, bytes):
                att_dict[key] = {"DataType": "Binary", "BinaryValue": value}
            else:
                raise ValueError(
                    f"Unsupported attribute value type: {type(value)}")
        return att_dict

    def _get_topic(self, name) -> str:
        """
        Gets a topic by its ARN.

        :param arn: The ARN of the topic to retrieve.
        :return: The topic, or None if not found.
        """
        try:
            if self._name_has_arn(name):
                arn = name
            else:
                region = self.sns_resource.meta.client.meta.region_name
                account = self.sts_client.get_caller_identity().get("Account")
                arn = f"arn:aws:sns:{region}:{account}:{name}"
            # topic = self.sns_resource.Topic(arn)
            # self.log.info("Got topic %s.", arn)
        except ClientError:
            self.log.exception("Couldn't get topic %s.", arn)
            raise
        else:
            return arn

    def _name_has_arn(self, name: str) -> bool:
        return name.startswith("arn:aws:sns:")
