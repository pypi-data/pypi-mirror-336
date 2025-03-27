from dataclasses import dataclass


@dataclass
class CommandError:
    """
    Clase para manejar los campos de error en el JSON de respuesta
    """

    codigo: str = "codigo"
    comando: str = "comando"
    mensaje: str = "mensaje"
