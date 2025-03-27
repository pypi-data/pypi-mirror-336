from arq_base_python.cqrs.core_api.src.messaging.message_serializer import (
    MessageSerializer,
)
from arq_base_python.cqrs.core_api.src.models.command_submitted import CommandSubmitted
from arq_base_python.cqrs.core_api.src.models.event_submitted import EventSubmitted
from arq_base_python.cqrs.core_api.src.models.submittable import Submittable
from arq_base_python.cqrs.core_api.src.models.command import Command
from arq_base_python.cqrs.core_api.src.models.event import Event
import json


class JsonMessageSerializer(MessageSerializer):
    def serialize(self, var1: object) -> str:
        return json.dumps(var1)

    def serialize_submittable(self, var1: Submittable) -> str:
        serialized = json.dumps(
            var1,
            default=lambda o: o.__dict__(),
            ensure_ascii=False)
        return serialized

    def parse_payload(self, var1: object, var2: type) -> object:
        try:
            if isinstance(var1, dict):
                return var2(**var1)
            return var2(var1)
        except Exception as e:
            raise Exception(f"Error parsing payload: {e}")

    def to_command_submitted(self, var1: str) -> CommandSubmitted:
        json_data: dict = json.loads(var1)
        comando = Command(**json_data["comando"])
        command_submitted = CommandSubmitted(
            comando=comando,
            validation_status=json_data["validationStatus"],
            validation_message=json_data["validationMessage"],
        )
        return command_submitted

    def to_event_submitted(self, var1: str) -> EventSubmitted:
        json_data: dict = json.loads(var1)
        evento = Event(**json_data["evento"])
        event_submitted = EventSubmitted(
            evento=evento,
            validation_status=json_data["validationStatus"],
            validation_message=json_data["validationMessage"],
        )
        return event_submitted
