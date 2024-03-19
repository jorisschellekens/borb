#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In computer science, a trie (/ˈtraɪ/, /ˈtriː/), also called digital tree or prefix tree, is a type of k-ary search tree,
a tree data structure used for locating specific keys from within a set. These keys are most often strings,
with links between nodes defined not by the entire key, but by individual characters.
In order to access a key (to recover its value, change it, or remove it), the trie is traversed depth-first,
following the links between nodes, which represent each character in the key.
"""
import typing


class Trie:
    """
    In computer science, a trie (/ˈtraɪ/, /ˈtriː/), also called digital tree or prefix tree, is a type of k-ary search tree,
    a tree data structure used for locating specific keys from within a set. These keys are most often strings,
    with links between nodes defined not by the entire key, but by individual characters.
    In order to access a key (to recover its value, change it, or remove it), the trie is traversed depth-first,
    following the links between nodes, which represent each character in the key.
    """

    class TrieNode:
        """
        This class represents a node in a trie
        """

        def __init__(self, value: typing.Optional[typing.Any] = None):
            self._children: typing.Dict[str, "Trie.TrieNode"] = {}
            self._value: typing.Optional[typing.Any] = value

        def __len__(self) -> int:
            return (0 if self._value is None else 1) + sum(
                [len(v) for k, v in self._children.items()]
            )

        def get_value(self) -> typing.Any:
            """
            This function returns the value of this TrieNode
            :return:    the value of this TrieNode
            """
            return self._value

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._root: typing.Optional[Trie.TrieNode] = None

    #
    # PRIVATE
    #

    def __getitem__(self, item) -> typing.Optional[typing.Any]:
        n: typing.Optional[Trie.TrieNode] = self._root
        if n is None:
            return None
        for c in item:
            # noinspection PyProtectedMember
            if c in n._children:
                # noinspection PyProtectedMember
                n = n._children[c]
            else:
                return None
        assert n is not None, "unexpected error while performing __getitem__ on Trie"
        return n.get_value()

    def __len__(self) -> int:
        return 0 if self._root is None else len(self._root)

    def __setitem__(self, key, value):
        n: typing.Optional[Trie.TrieNode] = self._root
        if n is None:
            self._root = Trie.TrieNode()
            n = self._root
        assert n is not None, "unexpected error while performing __setitem__ on Trie"
        for c in key:
            # noinspection PyProtectedMember
            if c not in n._children:
                # noinspection PyProtectedMember
                n._children[c] = Trie.TrieNode()
            # noinspection PyProtectedMember
            n = n._children[c]
        assert n is not None, "unexpected error while performing __setitem__ on Trie"
        n._value = value
        return self

    #
    # PUBLIC
    #
