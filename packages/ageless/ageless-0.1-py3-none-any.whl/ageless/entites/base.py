from typing import Dict, Type

from ageless.entites.property import AgePropertyCollection


class AgeEntity:
    # 标签，即传统数据库中的表名
    LABEL: str = ""
    # 名称，用于显示
    NAME: str = ""
    PROPERTY_CLS: Type[AgePropertyCollection] = None

    def __init__(self):
        self.id: str = ""
        self.properties: Dict = {}
