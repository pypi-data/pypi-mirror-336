from cqrs.core_api.src.models.base_serializable import BaseSerializable


class CommandSerializable(BaseSerializable):

    def deserialize(self, var1: str):
        raise IOError
