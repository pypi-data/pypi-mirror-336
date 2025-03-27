from enum import Enum


class EventResult(Enum):
    EXITO = 1
    FALLO = 2

    def get(self, result):
        try:
            return result
        except Exception:
            return self.EXITO
