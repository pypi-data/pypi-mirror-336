from dependency_injector import containers, providers
from arq_base_python.containers.command_handler_containers import ServiceDependencies, ValidatorDependencies
from arq_base_python.containers.yaml_reader import YAMLReader
from arq_base_python.cqrs.core.src.jms.receive_message_from_source import ReceiveMessageFromSource
from arq_base_python.adapters.aws.src.config.boto3_session_factory import Boto3SessionFactory, AsyncBoto3SessionFactory
from arq_base_python.adapters.aws.src.receive_message_from_sqs import ReceiveMessageFromSQS
from arq_base_python.cqrs.core.src.jms.async_executor_service import AsyncExecutorService
from arq_base_python.adapters.aws.src.config.aws_config import AwsListenerConfig
from arq_base_python.adapters.aws.src.aws_sns_init import AwsSNSInit


class ListenerDependencies(containers.DeclarativeContainer):
    config = providers.Configuration()
    service_dependencies: ServiceDependencies = providers.DependenciesContainer()
    validator_dependencies: ValidatorDependencies = providers.DependenciesContainer()

    async_executor_service = providers.Factory(
        AsyncExecutorService,
        serializer=service_dependencies.json_message_serializer,
        secured_application=service_dependencies.secured_application,
        send_message_to_mq=service_dependencies.send_message_to_mq,
        handler_resolver=validator_dependencies.handler_resolver)

    receive_message_from_source = providers.Factory(
        ReceiveMessageFromSource,
        send_message_to_mq=service_dependencies.send_message_to_mq,
        async_executor_service=async_executor_service)


class AWSSessionContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["application.yml"])

    session = providers.Singleton(
        Boto3SessionFactory,
        data=config,
    )

    async_session = providers.Singleton(
        AsyncBoto3SessionFactory,
        data=config,
    )


class SQSListenerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    yml_file = YAMLReader("application.yml").read()
    aws_session: AWSSessionContainer = providers.DependenciesContainer()
    listener_dependencies: ListenerDependencies = providers.DependenciesContainer()

    listener = providers.Factory(
        ReceiveMessageFromSQS,
        i_receive_message_from_source=listener_dependencies.receive_message_from_source,
        queue=config.server.mq.subscribeDestination,
        session=aws_session.session,
        region_name=config.cloud.aws.region.static,
        access_key=config.cloud.aws.credentials.accessKey,
        secret_key=config.cloud.aws.credentials.secretKey,
    )


class AWSConfigContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    aws_session: AWSSessionContainer = providers.DependenciesContainer()
    service_dependencies: ServiceDependencies = providers.DependenciesContainer()
    sqs_listener: SQSListenerContainer = providers.DependenciesContainer()

    aws_sns_init = providers.Factory(
        AwsSNSInit,
        aws_session=aws_session.session,
        destinations=service_dependencies.destinations)

    aws_config = providers.Factory(
        AwsListenerConfig,
        sqs_init=aws_sns_init,
        listener=sqs_listener.listener
    )


class AWSSQSListenerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    service_dependencies: ServiceDependencies = providers.DependenciesContainer()
    validator_dependencies: ValidatorDependencies = providers.DependenciesContainer()
    aws_session: AWSSessionContainer = providers.DependenciesContainer()

    listener_dependencies: ListenerDependencies = providers.Container(
        ListenerDependencies,
        config=config,
        service_dependencies=service_dependencies,
        validator_dependencies=validator_dependencies,)

    sqs_listener: SQSListenerContainer = providers.Container(
        SQSListenerContainer,
        config=config,
        aws_session=aws_session,
        listener_dependencies=listener_dependencies)

    aws_config_container: AWSConfigContainer = providers.Container(
        AWSConfigContainer,
        config=config,
        aws_session=aws_session,
        service_dependencies=service_dependencies,
        sqs_listener=sqs_listener)
