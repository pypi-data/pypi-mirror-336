
# Zona horaria para Colombia
from datetime import datetime
from zoneinfo import ZoneInfo


COLOMBIA_TIMEZONE = ZoneInfo("America/Bogota")


def localize_datetime(dt: datetime) -> datetime:
    """
    Asigna la zona horaria de Colombia a un datetime sin zona horaria.
    Si ya tiene zona horaria, lo convierte a la zona horaria de Colombia.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        # Si no tiene zona horaria, asignar la zona horaria de Colombia
        return dt.replace(tzinfo=COLOMBIA_TIMEZONE)
    else:
        # Si ya tiene zona horaria, convertir a la zona horaria de Colombia
        return dt.astimezone(COLOMBIA_TIMEZONE)


def format_datetime(dt: datetime) -> str:
    """
    Formatea un datetime como una cadena ISO 8601 con la zona horaria de Colombia.
    """
    if dt is None:
        return None

    localized_dt = localize_datetime(dt)
    return localized_dt.isoformat()
