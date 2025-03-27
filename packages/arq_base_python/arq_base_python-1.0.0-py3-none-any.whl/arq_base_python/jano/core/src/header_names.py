

from dataclasses import dataclass, field


@dataclass(init=False)
class HeaderNames:
    HEADER_CLIENTE_DNI: str = "ClienteDNI"

    HEADER_CLIENTE_DNI_MIN: str = "ClienteDNI".lower()

    HEADER_X_CLIENTE_DNI: str = f"x-{HEADER_CLIENTE_DNI_MIN}"

    HEADER_CUENTA_USUARIO: str = "CuentaUsuario"

    HEADER_CUENTA_USUARIO_MIN: str = "CuentaUsuario".lower()

    HEADER_X_CUENTA_USUARIO: str = f"x-{HEADER_CUENTA_USUARIO_MIN}"

    HEADER_CANAL: str = "canal"

    HEADER_X_CANAL: str = "x-canal"
