from ageless.operators.base import AgeOperator


class AgeIsNotNull(AgeOperator):
    name = "not_null"

    def serialize(self):
        return f"{self._entity_name}.{self._field} IS NOT NULL"
