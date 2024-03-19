#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    In computer science, a disjoint-set data structure, also called a union–find data structure or merge–find set,
    is a data structure that stores a collection of disjoint (non-overlapping) sets.
"""
import typing


class disjointset:
    """
    In computer science, a disjoint-set data structure, also called a union–find data structure or merge–find set,
    is a data structure that stores a collection of disjoint (non-overlapping) sets.
    Equivalently, it stores a partition of a set into disjoint subsets.
    It provides operations for adding new sets, merging sets (replacing them by their union),
    and finding a representative member of a set.
    The last operation allows to find out efficiently if any two elements are in the same or different sets.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._parents = {}
        self._ranks = {}

    #
    # PRIVATE
    #

    def __contains__(self, item):
        return item in self._parents

    def __iter__(self):
        return self._parents.__iter__()

    def __len__(self):
        return len(self._parents)

    #
    # PUBLIC
    #

    def add(self, x: typing.Any) -> "disjointset":
        """
        Add an element to this disjointset
        :param x:   the element to be added
        :return:    self
        """
        self._parents[x] = x
        self._ranks[x] = 0
        return self

    def find(self, x: typing.Any) -> typing.Any:
        """
        Find the root of an element in this disjointset
        :param x:   the element for which to find the root element
        :return:    the root element of the given element
        """
        if self._parents[x] == x:
            return x
        else:
            return self.find(self._parents[x])

    def pop(self, x: typing.Any) -> "disjointset":
        """
        Remove an element from this disjointset
        :param x:   the element to be removed
        :return:    self
        """
        raise NotImplementedError()

    def sets(self) -> typing.List[typing.List[typing.Any]]:
        """
        This function returns all equivalence sets in this disjointset
        :return:    all equivalence sets of this disjointset
        """
        cluster_parents: typing.Dict[typing.Any, typing.Any] = {}
        for x, _ in self._parents.items():
            p = self.find(x)
            if p not in cluster_parents:
                cluster_parents[p] = []
            cluster_parents[p].append(x)
        return [v for k, v in cluster_parents.items()]

    def union(self, x: typing.Any, y: typing.Any) -> "disjointset":
        """
        Mark two elements in this disjointset as equivalent,
        propagating the equivalence throughout the disjointset
        :param x:   the first element
        :param y:   the second element
        :return:    self
        """
        x_parent = self.find(x)
        y_parent = self.find(y)
        if x_parent is y_parent:
            return self
        if self._ranks[x_parent] > self._ranks[y_parent]:
            self._parents[y_parent] = x_parent
        elif self._ranks[y_parent] > self._ranks[x_parent]:
            self._parents[x_parent] = y_parent
        else:
            self._parents[y_parent] = x_parent
            self._ranks[x_parent] += 1
        return self
