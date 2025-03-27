import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed


# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# max_tries = 60 * 5  # 5 minutes
max_tries = 5
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
    reraise=True,
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main(engine) -> None:
    logger.info("Iniciando adaptador de base de datos")
    init(engine)
    logger.info("Adaptador de base de datos inicializado")
