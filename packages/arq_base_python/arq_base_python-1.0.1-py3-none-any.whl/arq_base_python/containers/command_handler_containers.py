from dependency_injector import containers, providers
from arq_base_python.entrypoints_base.command_receiver.src.commands.invalid_regex import (
    InvalidRegex,
)
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_body_validator import (
    CommandBodyValidator,
)
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_authorizer import (
    CommandAuthorizer,
)
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.rest_security_context_decorator import (
    RestSecurityContextDecorator,
)

from arq_base_python.jano.core.src.secured_application import SecuredApplication
from arq_base_python.entrypoints_base.command_receiver.src.commands.web.command_service import (
    CommandService,
)

from arq_base_python.cqrs.core.src.jms.message_publisher import MessagePublisher
from arq_base_python.cqrs.core.src.jms.send_message_to_mq import SendMessageToMQ
from arq_base_python.cqrs.core.src.jms.properties_creator import (
    PropertiesCreator,
)
from arq_base_python.cqrs.core_api.src.properties.mq_destinations import (
    MQDestinations,
)
from arq_base_python.cqrs.core.src.properties.developer_mode_props import (
    DeveloperModeProps,
)
from arq_base_python.adapters.aws.src.aws_sns_sender import AwsSnsSender
from arq_base_python.helpers.json_message_serializer.src.messaging.json_message_serializer import (
    JsonMessageSerializer,
)
from arq_base_python.cqrs.core.src.handlers.handler_resolver import HandlerResolver


class ValidatorDependencies(containers.DeclarativeContainer):
    config = providers.Configuration()
    handler_registry = providers.Dependency()

    invalid_regex = providers.Factory(
        InvalidRegex,
        default_regex=config.command,
    )

    handler_resolver = providers.Factory(
        HandlerResolver,
        registries=handler_registry,
    )


class ServiceDependencies(containers.DeclarativeContainer):
    config = providers.Configuration()
    aws_session = providers.DependenciesContainer()

    developer_mode_props = providers.Factory(
        DeveloperModeProps, developer_mode=config.server.mq.developerMode
    )
    json_message_serializer = providers.Factory(JsonMessageSerializer)
    destinations = providers.Factory(
        MQDestinations,
        publish_destination=config.server.mq.publishDestination,
        suscribre_destination=config.server.mq.suscribreDestination,
        ui_destination=config.server.mq.publishDestination,
    )
    aws_sns_sender = providers.Factory(
        AwsSnsSender,
        aws_session=aws_session.session,
        async_session=aws_session.async_session
    )
    secured_application = providers.Factory(
        SecuredApplication, config=config.securedApplication
    )
    security_helper = providers.Factory(
        RestSecurityContextDecorator, secured_application=secured_application
    )
    properties_creator = providers.Factory(
        PropertiesCreator, developer_node_props=developer_mode_props
    )
    send_message_to_mq = providers.Factory(
        SendMessageToMQ,
        properties_creator=properties_creator,
        mq_destinations=destinations,
        sender=aws_sns_sender,
        serializer=json_message_serializer,
    )
    message_publisher = providers.Factory(
        MessagePublisher, send_message_to_mq=send_message_to_mq
    )


class CommandValidatorContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    validator_dependencies: ValidatorDependencies = providers.DependenciesContainer()

    command_validator = providers.Factory(
        CommandBodyValidator,
        handler_registry=validator_dependencies.handler_registry,
        invalid_regex=validator_dependencies.invalid_regex,
    )


class CommandAuthorizerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    command_authorizer = providers.Factory(CommandAuthorizer)


class CommandServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    service_dependencies: ServiceDependencies = providers.DependenciesContainer()

    command_service = providers.Factory(
        CommandService,
        security_helper=service_dependencies.security_helper,
        message_publisher=service_dependencies.message_publisher,
        secured_application=service_dependencies.secured_application,
    )


class CommandHandlerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    aws_session = providers.DependenciesContainer()
    handler_registry = providers.Dependency()

    service_dependencies: ServiceDependencies = providers.Container(
        ServiceDependencies,
        config=config,
        aws_session=aws_session,
    )

    validator_dependencies: ValidatorDependencies = providers.Container(
        ValidatorDependencies,
        config=config,
        handler_registry=handler_registry,
    )

    command_validator_container: CommandValidatorContainer = providers.Container(
        CommandValidatorContainer,
        config=config,
        validator_dependencies=validator_dependencies,
    )

    command_authorizer_container: CommandAuthorizerContainer = providers.Container(
        CommandAuthorizerContainer,
        config=config,
    )

    command_service_container: CommandServiceContainer = providers.Container(
        CommandServiceContainer,
        config=config,
        service_dependencies=service_dependencies,
    )
