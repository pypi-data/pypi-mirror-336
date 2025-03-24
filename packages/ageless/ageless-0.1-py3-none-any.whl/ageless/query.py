from typing import Union, Optional, List

from ageless.criterion.edge import AgeEdgeCriteria
from ageless.criterion.path import PathCriteria
from ageless.criterion.vertex import AgeVertexCriteria


# engine = create_engine("", echo=True)
# Session = sessionmaker(bind=engine)


class AgeQuery:
    def __init__(self, graph_name: str):
        self._graph_name: str = graph_name
        self._paths: List[PathCriteria] = []
        self._find: Optional[Union[AgeVertexCriteria, AgeEdgeCriteria]] = None
        self._limit: Optional[int] = 10
        self._skip: Optional[int] = 0
        self._query: Optional[str] = None

    def match(self, path: PathCriteria):
        """
        匹配路径，可多次调用匹配复杂多分支路径
        :param path: 一条分支路径
        :return: 查询器实例
        """
        if self._find:
            raise ValueError(f"已指定find方法，不能再指定match方法")
        self._paths.append(path)
        return self

    def find(self, criteria: Union[AgeVertexCriteria, AgeEdgeCriteria]):
        """
        查询某一类实体列表，包括
        :param criteria:
        :return:
        """
        if self._find:
            raise ValueError("不能重复设置条件")
        if self._paths:
            raise ValueError(f"已指定match方法，不能再指定find方法")
        if not isinstance(criteria, AgeVertexCriteria) and not isinstance(criteria, AgeEdgeCriteria):
            raise ValueError(f"criteria参数只支持AgeVertexCriteria和AgeEdgeCriteria类型")
        self._find = criteria
        return self

    def limit(self, size):
        if size > 1000:
            raise ValueError("一次返回数量不得超过1000条")
        self._limit = size
        return self

    def skip(self, count):
        self._skip = count
        return self

    def _build_find(self):
        clauses = [f"MATCH {self._find.serialize()}"]
        if self._find.order_bys:
            clauses.append(
                f"ORDER BY {', '.join([order_by.serialize() for order_by in self._find.order_bys.values()])}"
            )
        clauses.append(f"SKIP {self._skip}")
        clauses.append(f"LIMIT {str(self._limit)}")
        if self._find.queries:
            clauses.append(f"WHERE {', '.join([query.serialize() for query in self._find.queries])}")
        if self._find.return_fields:
            clauses.append(
                f"RETURN {', '.join([f'{self._find.name}.{return_field}' for return_field in self._find.return_fields])}"
            )
        match_clause = " ".join(clauses)
        return f"""SELECT * FROM cypher('{self._graph_name}', $$
            {match_clause}
            $$) as (a agtype);"""

    def build(self):
        if self._find:
            return self._build_find()


if __name__ == "__main__":
    query_ = AgeQuery("test_age")
    vertex = AgeVertexCriteria("aaa")
    vertex.label("test_label").order_by("a_field").returns("a_field").filter(a_field__ne="aaa")
    aa = query_.find(vertex).limit(10).skip(1).build()
    print(aa)
