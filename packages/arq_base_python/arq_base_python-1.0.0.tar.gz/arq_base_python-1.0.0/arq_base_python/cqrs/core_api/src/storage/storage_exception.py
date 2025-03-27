from cqrs.core_api.src.exceptions.technical_exception import TechnicalException


class StorageException(TechnicalException):
    def __init__(self, message, detalle=None):
        super().__init__(message, detalle)

    def __str__(self):
        return f"StorageException(super={super().__str__()})"
