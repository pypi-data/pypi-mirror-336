import os
import pkgutil
from dependency_injector import containers, providers
from arq_base_python.app.logging import logging
from arq_base_python.adapters.aws_s3.aws_s3_containers import AwsS3Container
from arq_base_python.containers.aws_containers import (
    AWSSessionContainer, AWSSQSListenerContainer)
from arq_base_python.containers.command_handler_containers import CommandHandlerContainer
from arq_base_python.entrypoints_base.storage_rest_api.fileapi.config.storage_containers import StorageContainer
# from arq_base_python.configuration.microservice.src.application_handler import ApplicationHandler


def get_own_packages():
    paquetes = []
    exlude = ["venv"]
    # Obtener el nombre de la carpeta donde se encuentra el script principal
    carpeta_principal = os.path.dirname("main.py")
    for _, nombre, _ in pkgutil.iter_modules():
        # Comprobar si el paquete está dentro de la carpeta principal
        ruta_paquete = os.path.join(carpeta_principal, nombre)
        if os.path.isdir(ruta_paquete) and nombre not in exlude:
            paquetes.append(nombre)
    return paquetes


class Application(containers.DeclarativeContainer):
    log = logging.getLogger(__name__)
    log.debug("Iniciando contenedores")

    wiring_config = containers.WiringConfiguration(packages=get_own_packages())
    config = providers.Configuration(yaml_files=["application.yml"])
    application_handler = providers.DependenciesContainer()

    # AWS Containers
    aws_session: AWSSessionContainer = providers.Container(
        AWSSessionContainer,
    )

    # S3 Storage Containers
    aws_s3_container: AwsS3Container = providers.Container(
        AwsS3Container,
    )

    storage_container: StorageContainer = providers.Container(
        StorageContainer,
    )

    # Application Containers
    # application_handler: ApplicationHandler = providers.Container(
    #     ApplicationHandler,
    # )

    command_handler_container: CommandHandlerContainer = providers.Container(
        CommandHandlerContainer,
        config=config,
        aws_session=aws_session,
        handler_registry=application_handler.handler_registry,)

    # SQS Listener Containers
    listener_container: AWSSQSListenerContainer = providers.Container(
        AWSSQSListenerContainer,
        config=config,
        aws_session=aws_session,
        service_dependencies=command_handler_container.service_dependencies,
        validator_dependencies=command_handler_container.validator_dependencies,)
