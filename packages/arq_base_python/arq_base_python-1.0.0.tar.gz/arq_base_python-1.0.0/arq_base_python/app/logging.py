import logging
import logging.config
LOG_FORMAT = "%(levelprefix)s [%(asctime)s] >>> %(module)s:%(lineno)d - %(message)s"
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "use_colors": True,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stderr"
        },
        # Descomenta esto si deseas usar un archivo de registro
        # "file": {
        #     "class": "logging.handlers.TimedRotatingFileHandler",
        #     "formatter": "default",
        #     "filename": "logs/fastapi-efk.log",
        #     "when": "midnight",
        #     "backupCount": 5,
        # },
    },
    "root": {
        "level": "DEBUG",
        # Agrega "file" si deseas usar un archivo de registro
        "handlers": ["console"],
    },
    "loggers": {}
}

# Lista de loggers a excluir
excluded_loggers = [
    "botocore",
    "boto3",
    "aiobotocore",
    "faker",
    "urllib3"
    # Agrega más loggers aquí si es necesario
]

for logger_name in excluded_loggers:
    logging_config["loggers"][logger_name] = {
        "level": "WARNING",
        "handlers": ["console"],
        "propagate": False
    }


logging.config.dictConfig(logging_config)
