from ageless.criterion.edge import AgeEdgeCriteria
from ageless.criterion.vertex import AgeVertexCriteria


class PathCriteria:
    def __init__(self):
        self._sequence = []

    def vertex(self, vertex_criteria: AgeVertexCriteria):
        self._sequence.append(vertex_criteria)
        return self

    def edge(self, edge_criteria: AgeEdgeCriteria):
        self._sequence.append(edge_criteria)
        return self
