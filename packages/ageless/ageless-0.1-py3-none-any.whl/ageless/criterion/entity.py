import random
import string
from abc import ABC
from typing import Union, Tuple, List, Dict

from ageless.criterion.q import AgeQ, AgeOrderBy, OrderByType
from ageless.operators.runtime import operator_manager
from ageless.serializable import AgeSerializable


class AgeEntityCriteria(AgeSerializable, ABC):
    _LEFT_IDENTIFIER: str = None
    _RIGHT_IDENTIFIER: str = None

    def __init__(self, name: str = ""):
        self.name = name or self.generate_random_sequence(8)

        self.label_name: str = ""
        self.queries: Union[List[AgeQ], Tuple[AgeQ]] = []
        self.order_bys: Dict[str, AgeOrderBy] = {}
        self.return_fields: List[str] = []

    @staticmethod
    def generate_random_sequence(length):
        # string.ascii_letters 包含所有大小写字母
        return ''.join(random.choices(string.ascii_letters, k=length))

    # 指定检索的点或边的label
    def label(self, label: str):
        self.label_name = label
        return self

    # 加入检索条件
    def filter(self, *args: AgeQ, **kwargs: Dict[str, object]):
        self.queries.extend(args)
        for k, v in kwargs.items():
            k_split = k.split("__")
            if len(k_split) == 1:
                field = k
                op = "eq"
            elif len(k_split) == 2:
                field = k_split[0]
                op = k_split[1]
            else:
                raise ValueError(f"{k}:参数形式错误")
            op_cls = operator_manager.get(op)
            self.queries.append(op_cls(self.name, field, v))
        return self

    def returns(self, field_or_fields: Union[List[str], str]):
        if isinstance(field_or_fields, str):
            self.return_fields.append(field_or_fields)
        else:
            self.return_fields.extend(field_or_fields)
        return self

    def order_by(self, field: str, order_by_type: OrderByType = OrderByType.ASC):
        self.order_bys[field] = AgeOrderBy(self.name, field, order_by_type)
        return self

    def serialize(self):
        if self.label_name:
            return f"{self._LEFT_IDENTIFIER}{self.name}:{self.label_name}{self._RIGHT_IDENTIFIER}"
        else:
            return f"{self._LEFT_IDENTIFIER}{self.name}{self._RIGHT_IDENTIFIER}"
