from abc import ABC

from ageless.serializable import AgeSerializable


class AgeOperator(AgeSerializable, ABC):
    name: str = None
    text: str = None

    def __init__(self, entity_name: str, field: str, value: object = None):
        self._entity_name: str = entity_name
        self._field: str = field
        self._value: object = value
