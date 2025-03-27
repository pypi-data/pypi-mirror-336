import logging
from boto3 import Session
from botocore.exceptions import ClientError
from arq_base_python.cqrs.core_api.src.properties.destinations import (
    Destinations,
)


class AwsSNSInit:
    def __init__(self, aws_session: Session, destinations: Destinations) -> None:
        self.log = logging.getLogger(__name__)
        self._session = aws_session
        self.log.info("Verificando sesión de AWS")
        self.validate_aws_session()
        self._destinations = destinations
        self._dict_topics = self._get_topics()
        self.log.info("Inicializando configuración de SNS")
        # self._initialize_topic()

    def validate_aws_session(self):
        try:
            # Crear un cliente de STS (AWS Security Token Service)
            sts_client = self._session.client('sts')

            # Intentar obtener la identidad del usuario
            identity = sts_client.get_caller_identity()

            # Si la llamada tiene éxito, las credenciales son válidas
            print(
                f"Sesión AWS creada exitosamente. User ID: {identity['UserId']}")
            arn_identity = self._session.client(
                'sts').get_caller_identity()['Arn']
            self.log.info(f"El ARN del usuario es: {arn_identity}")
        except ClientError as e:
            # Manejar errores específicos
            if e.response['Error']['Code'] == 'InvalidClientTokenId':
                raise ValueError("Las credenciales de AWS son inválidas")
            elif e.response['Error']['Code'] == 'ExpiredToken':
                raise ValueError("Las credenciales de AWS han expirado")
            elif e.response['Error']['Code'] == 'AccessDenied':
                raise ValueError(
                    "El usuario no tiene permisos para acceder a AWS")
            else:
                # Re-lanzar la excepción si es otro tipo de error
                raise e

    def _get_topics(self) -> dict:
        temp_topics = {
            self._destinations.get_publish_destination(): False
        }
        return temp_topics

    def _initialize_topic(self):
        # Crear un cliente de SNS
        sns_client = self._session.client('sns')
        # Construir el ARN del tópico
        account_id = self._session.client(
            'sts').get_caller_identity()['Account']
        arn_without_topic_name = f'arn:aws:sns:{self._session.region_name}:{account_id}:'
        for topic_name in self._dict_topics.keys():
            try:
                # Intentar obtener los atributos del tópico
                sns_client.get_topic_attributes(
                    TopicArn=arn_without_topic_name + topic_name)
                self.log.info(f"El tópico {topic_name} existe")
                self._dict_topics[topic_name] = True
            except ClientError as e:
                # Manejo de errores específicos
                if e.response['Error']['Code'] == 'NotFound':
                    raise ValueError(f"El tópico {topic_name} no existe")
                elif e.response['Error']['Code'] == 'AuthorizationError':
                    raise ValueError(
                        f"El usuario no tiene permisos para acceder al tópico {topic_name}")
                elif e.response['Error']['Code'] == 'InvalidParameter':
                    raise ValueError(
                        f"El ARN del tópico {topic_name} es inválido")
                else:
                    # Re-lanzar la excepción si es otro tipo de error
                    raise e
