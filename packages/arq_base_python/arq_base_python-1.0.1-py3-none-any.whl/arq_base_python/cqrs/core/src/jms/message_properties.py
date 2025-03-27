from typing import Dict


class MessageProperties:
    def __init__(self):
        self.props: Dict[str, str] = {}

    @staticmethod
    def create():
        return MessageProperties()

    def add(self, property, value):
        if property is not None and value is not None:
            self.props[property] = value
        return self

    def add_if(self, condition, prop, supplier: callable):
        if condition:
            self.add(prop, supplier())
        return self

    def get_properties(self) -> Dict[str, str]:
        return self.props

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(props={self.get_properties()})"
