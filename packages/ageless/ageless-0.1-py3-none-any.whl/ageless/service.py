import re
from typing import Type, Dict, Union

from ageless.entites.edge import AgeEdge
from ageless.entites.vertext import AgeVertex


class AgeRegistry:
    _VERTEX_LABEL_REG = re.compile(r"^[A-Z][A-Za-z]*$")
    _RELATION_LABEL_REG = re.compile(r"^[A-Za-z_]*$")

    def __init__(self):
        self._vertices: Dict[str, Type[AgeVertex]] = {}
        self._edges: Dict[str, Type[AgeEdge]] = {}

    def register(self, age_entity_type: Union[Type[AgeVertex], Type[AgeEdge]]):
        if issubclass(age_entity_type, AgeVertex):
            label = age_entity_type.LABEL
            if not self._VERTEX_LABEL_REG.match(label):
                raise ValueError("顶点类型LABEL必须以大写字母开头，全部为大小写字母，驼峰命名")
            self._vertices[age_entity_type.LABEL] = age_entity_type
        elif issubclass(age_entity_type, AgeEdge):
            label = age_entity_type.LABEL
            if not self._RELATION_LABEL_REG.match(label):
                raise ValueError("关系类型LABEL只能包括大写字母和下划线，大写蛇形命名")
        else:
            raise ValueError("不支持的实体类型")


age_registry = AgeRegistry()
