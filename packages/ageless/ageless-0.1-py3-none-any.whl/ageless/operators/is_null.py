from ageless.operators.base import AgeOperator


class AgeIsNull(AgeOperator):
    name = "null"

    def serialize(self):
        return f"{self._entity_name}.{self._field} IS NULL"
