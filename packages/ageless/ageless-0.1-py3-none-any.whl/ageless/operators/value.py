from abc import ABC

from ageless.operators.base import AgeOperator


class AgeValueOperator(AgeOperator, ABC):
    def serialize(self):
        if type(self._value) == str:
            value = f"\'{self._value}\'"
        else:
            value = self._value
        return f"{self._entity_name}.{self._field} {self.text} {value}"
