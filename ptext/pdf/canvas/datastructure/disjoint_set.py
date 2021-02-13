import typing
from typing import List, Any


class disjointset:
    """
    In computer science, a disjoint-set data structure, also called a union–find data structure or merge–find set,
    is a data structure that stores a collection of disjoint (non-overlapping) sets.
    Equivalently, it stores a partition of a set into disjoint subsets.
    It provides operations for adding new sets, merging sets (replacing them by their union),
    and finding a representative member of a set.
    The last operation allows to find out efficiently if any two elements are in the same or different sets.
    """

    def __init__(self):
        self.parents = {}
        self.ranks = {}

    def find(self, x: Any) -> Any:
        """
        Find the root of an element in this disjointset
        """
        if self.parents[x] == x:
            return x
        else:
            return self.find(self.parents[x])

    def union(self, x: Any, y: Any) -> "disjointset":
        x_parent = self.find(x)
        y_parent = self.find(y)
        if x_parent is y_parent:
            return self
        if self.ranks[x_parent] > self.ranks[y_parent]:
            self.parents[y_parent] = x_parent
        elif self.ranks[y_parent] > self.ranks[x_parent]:
            self.parents[x_parent] = y_parent
        else:
            self.parents[y_parent] = x_parent
            self.ranks[x_parent] += 1
        return self

    def add(self, x: Any) -> "disjointset":
        self.parents[x] = x
        self.ranks[x] = 0
        return self

    def pop(self, x: Any) -> "disjointset":
        # TODO
        return self

    def sets(self) -> List[List[Any]]:
        cluster_parents: typing.Dict[Any, Any] = {}
        for x, _ in self.parents.items():
            p = self.find(x)
            if p not in cluster_parents:
                cluster_parents[p] = []
            cluster_parents[p].append(x)
        return [v for k, v in cluster_parents.items()]

    def __len__(self):
        return len(self.parents)

    def __contains__(self, item):
        return item in self.parents
