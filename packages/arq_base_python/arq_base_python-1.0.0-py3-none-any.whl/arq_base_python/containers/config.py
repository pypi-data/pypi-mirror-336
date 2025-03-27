from dependency_injector.wiring import Provide, inject
from containers.application_container import Application
from adapters.aws.src.config.aws_config import AwsListenerConfig
from adapters.aws.src.receive_message_from_sqs import ReceiveMessageFromSQS


@inject
class ListenerConfig:
    def __init__(self,
                 aws_config: AwsListenerConfig = Provide[Application.listener_container.aws_config_container.aws_config]):
        self._aws_config = aws_config

    def get_aws_listener(self) -> ReceiveMessageFromSQS:
        return self._aws_config.get_listener()
