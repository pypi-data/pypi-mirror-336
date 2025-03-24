from typing import Dict, Type

from ageless.operators.base import AgeOperator


class AgeOperatorManager:
    def __init__(self):
        self._operators: Dict[str, Type[AgeOperator]] = {}

    def register(self, op_cls: Type[AgeOperator]):
        self._operators[op_cls.name] = op_cls

    def get(self, op_name: str):
        return self._operators[op_name]