from ageless.operators.base import AgeOperator


class AgeRaw(AgeOperator):
    name = "raw"

    def serialize(self):
        return f"{self._entity_name}.{self._field} {self._value}"
