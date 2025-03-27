import psycopg
import subprocess
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from arq_base_python.containers.config import ListenerConfig
from arq_base_python.adapters.settings import yaml_settings
from arq_base_python.adapters.database.src.config.db import engine
from arq_base_python.adapters.database.src.db_connection import main as db_connection
from arq_base_python.containers.s3_init import S3Init


def test_db_connection_with_iam_token():
    ENDPOINT = yaml_settings.repository.database.host
    PORT = yaml_settings.repository.database.port
    USER = yaml_settings.repository.database.user
    REGION = "us-east-1"
    DBNAME = yaml_settings.repository.database.name
    DBSCHEMA = yaml_settings.repository.database.schema_name
    SSL_MODE = "verify-ca"
    SSL_PATH = "./app/us-east-1-bundle.pem"

    session = yaml_settings.get_session
    client = session.client('rds')

    token = client.generate_db_auth_token(
        DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

    try:
        # Con certificado SSL
        print("--Connecting to the database--")
        with psycopg.connect(conninfo=f"host={ENDPOINT} port={PORT} dbname={DBNAME} user={USER} password={token} options='-c search_path={DBSCHEMA}' sslmode={SSL_MODE} sslrootcert={SSL_PATH}") as conn:
            # Fetch the current schema and list of tables
            query = """
                SELECT current_schema(), table_name
                FROM information_schema.tables
                WHERE table_schema = current_schema();
            """

            result = conn.execute(query).fetchall()
            print('Tables', result)
            # task_data = conn.execute("SELECT * FROM task").fetchall()
            # print('Task data', task_data)
        print("--Connection successful--")
    except Exception as e:
        print("--Database connection failed due to {}".format(e))


def active_listener():
    app_config = ListenerConfig()

    # Iniciar el listener de SQS
    # * Usando thread y asyncio
    receive_message_from_sqs = app_config.get_aws_listener()
    receive_message_from_sqs.start_thread()
    # # Iniciar el listener de SQS en un hilo separado
    receive_message_from_sqs.run_listener()


class AlembicMigrationError(Exception):
    pass


async def run_alembic_migrations():
    """Ejecuta las migraciones de Alembic."""
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
    except Exception as e:
        raise AlembicMigrationError(e)


# Función de inicio y fin del ciclo de vida de la aplicación FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    log = logging.getLogger(__name__)

    # Iniciar S3 bucket
    # S3Init()

    # Iniciar el listener de SQS en un hilo
    try:
        active_listener()
    except Exception as e:
        log.error(f"Error al iniciar el listener de SQS: {e}")

    # test_db_connection_with_iam_token()
    # Conectar a la base de datos y realizar las migraciones de Alembic
    if engine:
        try:
            log.info(
                "Repositorio de datos habilitado, conectando a la base de datos...")
            db_connection(engine)
            log.info("Conexión exitosa a la base de datos.")
            log.info("Ejecutando migraciones de Alembic...")
            await run_alembic_migrations()
        except AlembicMigrationError as e:
            log.error(f"Error al ejecutar las migraciones de Alembic: {e}")
        except Exception as e:
            log.error(f"Fallo la conexión a la base de datos: {e}")
    else:
        log.warning("No se ha habilitado el repositorio de datos.")

    yield  # Aquí se permite que FastAPI maneje la ejecución hasta el shutdown

    # Funciones de limpieza después de que la aplicación se cierre
    log.info("Aplicación cerrada. Limpiando recursos...")
