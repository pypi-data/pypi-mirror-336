from boto3 import Session
from adapters.aws.src.receive_message_from_sqs import ReceiveMessageFromSQS
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from adapters.aws.src.aws_sns_init import AwsSNSInit


class AwsListenerConfig():
    def __init__(self,  sqs_init: AwsSNSInit, listener: ReceiveMessageFromSQS) -> None:
        self._listener = listener

    def get_listener(self):
        return self._listener
