from dataclasses import dataclass, fields


@dataclass
class CommandAck:
    id: str
    nombre: str
    idTrazabilidad: str
    appId: str
    username: str
    idSession: str
    timestamp: int

    def build_response(self):
        response = {}
        for field in fields(self):
            response[field.name] = getattr(self, field.name)
        return response
