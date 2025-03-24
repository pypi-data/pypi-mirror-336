from abc import ABC
from typing import Union, List, Tuple

from ageless.serializable import AgeSerializable


class AgeQ(AgeSerializable, ABC):
    pass


class AgeOR(AgeQ):
    def __init__(self, *args):
        self._queries: Union[List[AgeQ], Tuple[AgeQ]] = list(args)

    def serialize(self):
        return " AND ".join([q.serialize() for q in self._queries])


class AgeAnd(AgeQ):
    def __init__(self, *args):
        self._queries: Union[List[AgeQ], Tuple[AgeQ]] = list(args)

    def serialize(self):
        return " OR ".join([q.serialize() for q in self._queries])


class OrderByType:
    ASC = "asc"
    DESC = "desc"


class AgeOrderBy(AgeSerializable):
    def __init__(self, entity_name: str, field_name: str, order_by_type: OrderByType):
        self._entity_name: str = entity_name
        self._field_name: str = field_name
        self._type: OrderByType = order_by_type

    def serialize(self):
        if self._type == OrderByType.ASC:
            return f"{self._entity_name}.{self._field_name}"
        else:
            return f"{self._entity_name}.{self._field_name} DESC"
