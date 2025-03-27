from boto3 import Session
from aioboto3.session import Session as AsyncSession
import logging


def get_aws_credentials_and_region(data: dict) -> tuple:
    aws_access_key = data.get("cloud", {}).get(
        "aws", {}).get("credentials", {}).get("accessKey")
    aws_secret_key = data.get("cloud", {}).get(
        "aws", {}).get("credentials", {}).get("secretKey")
    region = data.get("cloud", {}).get("aws", {}).get("region", {}).get(
        "static", 'us-east-1')  # Default to 'us-east-1' if not set
    return aws_access_key, aws_secret_key, region


def create_session(session_class, data: dict) -> Session | AsyncSession:
    aws_access_key, aws_secret_key, region = get_aws_credentials_and_region(
        data)
    log = logging.getLogger(__name__)

    if aws_access_key and aws_secret_key:
        log.info(f"Creando sesión con credenciales de acceso")
        return session_class(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
    else:
        log.info(f"Creando sesión con credenciales de web, region: {region}")
        return session_class(region_name=region)


class Boto3SessionFactory(Session):
    def __init__(self, data):
        session = create_session(Session, data)
        self.__dict__.update(session.__dict__)

    def get_session(self) -> Session:
        return self


class AsyncBoto3SessionFactory(AsyncSession):
    def __init__(self, data):
        session = create_session(AsyncSession, data)
        self.__dict__.update(session.__dict__)

    def get_session(self) -> AsyncSession:
        return self
