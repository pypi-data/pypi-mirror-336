import logging
from pydantic_core import MultiHostUrl
from boto3 import Session
from typing import Self, Optional
from urllib.parse import quote


# Excepciones personalizadas para manejar errores en la generación de tokens
class DatabaseTokenGenerationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


# Clase para generar la cadena de conexión a la base de datos
class DatabaseConnectionFactory:
    def __init__(self, host: str, port: int, user: str, password: Optional[str], database: str, schema: str, session: Session):
        self.log = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema
        self.session = session

    def get_connection_string(self, develperMode: bool = True) -> str:
        """Genera el DSN para la conexión a la base de datos."""
        if develperMode is False:
            self.log.info("Conexión a la base de datos usando: IAM ROLES")
            return self.get_iam_connection_string()

        self.log.info("Conexión a la base de datos usando: USER/PASSWORD")
        return self.get_password_connection_string()

    def get_iam_connection_string(self) -> str:
        """Genera un DSN usando un token IAM en lugar de una contraseña."""
        try:
            token = self.generate_rds_iam_token()
            encoded_token = quote(token, safe='')
            return str(MultiHostUrl.build(
                scheme="postgresql+psycopg",
                username=self.user,
                password=encoded_token,
                host=self.host,
                port=self.port,
                path=self.database,
                query=f'options=-c search_path={self.schema}&sslmode=verify-ca&sslrootcert=./app/us-east-1-bundle.pem',
            ))
        except Exception as e:
            raise DatabaseTokenGenerationError(
                f"Error al generar el token IAM: {e}")

    def get_password_connection_string(self) -> str:
        """Genera un DSN usando una contraseña directamente."""
        return str(MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.database,
            query=f'options=-c search_path={self.schema}&gssencmode=disable',
        ))

    def generate_rds_iam_token(self) -> str:
        """Genera el token IAM para la autenticación con RDS."""
        try:
            client = self.session.client('rds')
            return client.generate_db_auth_token(
                DBHostname=self.host,
                Port=self.port,
                DBUsername=self.user,
                Region='us-east-1',
            )
        except Exception as e:
            raise DatabaseTokenGenerationError(
                f"Error al generar el token IAM: {e}")
