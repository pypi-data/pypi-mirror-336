import logging


class InvalidRegex:
    global_regex = r"[~!@#&|;'?/*$^+\\<>]"

    def __init__(self, default_regex: dict = None):
        self.log = logging.getLogger(__name__)
        self.default_regex = default_regex if default_regex is not None else {}
        self.regex_id = self._add_brackets(
            self.default_regex.get("id", self.global_regex)
        )
        self.regex_nombre = self._add_brackets(
            self.default_regex.get("nombre", self.global_regex)
        )
        self.regex_id_trazabilidad = self._add_brackets(
            self.default_regex.get("idTrazabilidad", self.global_regex)
        )
        self.regex_version = self._add_brackets(
            self.default_regex.get("version", self.global_regex)
        )
        self.regex_aplicacion_emisora = self._add_brackets(
            self.default_regex.get("aplicacionEmisora", self.global_regex)
        )
        self.regex_aplicacion_origen = self._add_brackets(
            self.default_regex.get("aplicacionOrigen", self.global_regex)
        )
        self.regex_usuario = self._add_brackets(
            self.default_regex.get("usuario", self.global_regex)
        )
        self.regex_dni = self._add_brackets(
            self.default_regex.get("dni", self.global_regex)
        )
        self.regex_timestamp = self._add_brackets(
            self.default_regex.get("timestamp", self.global_regex)
        )
        self.regex_payload = self._add_brackets(
            self.default_regex.get("payload", self.global_regex)
        )

    def print_regex(self) -> dict:
        return {
            "id": self.regex_id,
            "nombre": self.regex_nombre,
            "id_trazabilidad": self.regex_id_trazabilidad,
            "version": self.regex_version,
            "aplicacion_emisora": self.regex_aplicacion_emisora,
            "aplicacion_origen": self.regex_aplicacion_origen,
            "usuario": self.regex_usuario,
            "dni": self.regex_dni,
            "timestamp": self.regex_timestamp,
            "payload": self.regex_payload,
            "default_regex": self.default_regex,
        }

    def get_regex(self, key: str) -> str:
        if key == "id":
            return self.regex_id
        elif key == "nombre":
            return self.regex_nombre
        elif key == "idTrazabilidad":
            return self.regex_id_trazabilidad
        elif key == "version":
            return self.regex_version
        elif key == "aplicacionEmisora":
            return self.regex_aplicacion_emisora
        elif key == "aplicacionOrigen":
            return self.regex_aplicacion_origen
        elif key == "usuario":
            return self.regex_usuario
        elif key == "dni":
            return self.regex_dni
        elif key == "timestamp":
            return self.regex_timestamp
        elif key == "payload":
            return self.regex_payload
        else:
            return self.global_regex

    def _add_brackets(self, regex: str) -> str:
        if not regex.startswith("[") and not regex.endswith("]"):
            return f"[{regex}]"
        return regex
