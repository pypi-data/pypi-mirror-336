# ================
# start imports
# ================

import json
import logging
import os
import sys
import time
from abc import ABCMeta, abstractmethod

import boto3
import boto3.session
import aioboto3
from botocore.exceptions import ClientError
import boto3.exceptions
import threading
import asyncio


# ================
# start class
# ================


class SqsListener:
    __metaclass__ = ABCMeta

    def __init__(self, queue, **kwargs):
        """
        :param queue: (str) name of queue to listen to
        :param kwargs: options for fine tuning. see below
        """
        boto3_session = kwargs.get("session", None)
        if not boto3_session:
            raise boto3.exceptions.Boto3Error("No boto3 session was found")

        self.log = logging.getLogger(__name__)
        self.log.debug("Inicializando SQS Listener...")
        self._access_key = kwargs.get("access_key", None)
        self._secret_key = kwargs.get("secret_key", None)
        self._queue_name = queue
        self._poll_interval = kwargs.get("interval", 3)
        self._queue_visibility_timeout = kwargs.get(
            "visibility_timeout", "600")
        self._error_queue_name = kwargs.get("error_queue", None)
        self._error_queue_visibility_timeout = kwargs.get(
            "error_visibility_timeout", "600"
        )
        self._queue_url = kwargs.get("queue_url", None)
        self._message_attribute_names = kwargs.get(
            "message_attribute_names", [])
        self._attribute_names = kwargs.get("attribute_names", [])
        self._force_delete = kwargs.get("force_delete", False)
        self._endpoint_name = kwargs.get("endpoint_name", None)
        self._wait_time = kwargs.get("wait_time", 1)
        self._max_number_of_messages = kwargs.get("max_number_of_messages", 1)
        self._deserializer = kwargs.get("deserializer", json.loads)

        # must come last
        self._session = boto3_session
        self._region_name = kwargs.get("region_name")
        self._client = self._initialize_client()
        self.log.info(f"SQS listener inicializado para {self._queue_name}")
        self.loop = asyncio.new_event_loop()

    def _initialize_client(self):
        # new session for each instantiation
        ssl = True
        if self._region_name == "elasticmq":
            ssl = False
        sqs = self._session.client(
            "sqs",
            region_name=self._region_name,
            endpoint_url=self._endpoint_name,
            use_ssl=ssl,
        )

        try:
            qs = sqs.get_queue_url(QueueName=self._queue_name)
            self._queue_url = qs["QueueUrl"]
        except ClientError as e:
            raise e
        return sqs

    async def _start_sqs_listener_better(self, stop_=None):
        session = aioboto3.Session(region_name=self._region_name,
                                   aws_access_key_id=self._access_key,
                                   aws_secret_access_key=self._secret_key)
        try:
            async with session.client("sqs") as sqs:
                while True:
                    if stop_ and stop_.is_set():
                        break
                    try:
                        response = await sqs.receive_message(
                            QueueUrl=self._queue_url,
                            MessageAttributeNames=[
                                'tipo', 'type', 'dev', 'id', 'timestamp'],
                            MaxNumberOfMessages=self._max_number_of_messages,
                            WaitTimeSeconds=self._wait_time
                        )
                    except Exception as e:
                        self.log.error(
                            f">>>>Error al obtener mensaje de la cola: {self._queue_url}, error: {e}")

                    # Procesar los mensajes
                    messages = response.get('Messages', [])
                    for message in messages:
                        message_atrib = self._parse_message_attributes(
                            message.get('MessageAttributes', {})
                        )

                        # Eliminar el mensaje de la cola
                        await sqs.delete_message(
                            QueueUrl=self._queue_url,
                            ReceiptHandle=message['ReceiptHandle']
                        )

                        self.handle_message(message['Body'], message_atrib)

                    # Espera un momento antes de la siguiente solicitud para no sobrecargar la cola
                    await asyncio.sleep(0)
        except Exception as e:
            self.log.error(f">>>>Error creando el cliente: {e}")

    def _parse_message_attributes(self, message_attributes):
        """
        Parse message attributes from SQS response
        :param message_attributes: dict
        :return: dict
        """
        return {
            key: value.get("StringValue")
            for key, value in message_attributes.items()
        }

    def start_thread(self):
        """
        Create a new thread and run a new event loop in it
        """
        threading.Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_listener(self):
        """
        Execute the SQS Listener coroutine in the event loop provided by the thread
        """
        asyncio.run_coroutine_threadsafe(
            self._start_sqs_listener_better(), self.loop)

    @abstractmethod
    def handle_message(self, body, messages_attributes):
        """
        Implement this method to do something with the SQS message contents
        :param body: dict
        :param attributes: dict
        :param messages_attributes: dict
        :return:
        """
        return
