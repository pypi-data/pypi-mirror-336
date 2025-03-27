import uuid


class TechnicalException(Exception):
    def __init__(self, message=None, detalle_interno=None):
        super().__init__(message)
        self.uuid = str(uuid.uuid4())
        self.message = message
        self.detalle_interno = detalle_interno

    def __str__(self):
        return f"TechnicalException(uuid={self.uuid}, message={self.message}, detalle_interno={self.detalle_interno})"

    def get_uuid(self):
        return self.uuid

    def get_message(self):
        return self.message

    def get_detalle_interno(self):
        return self.detalle_interno
