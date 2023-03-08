#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a trie[str, typing.Any]
"""
import typing


class Trie:
    """
    This class represents a trie[str, typing.Any]
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
            if c in n._children:
                n = n._children[c]
            else:
                return None
        assert n is not None, "unexpected error while performing __getitem__ on Trie"
        return n._value

    def __len__(self) -> int:
        return 0 if self._root is None else len(self._root)

    def __setitem__(self, key, value):
        n: typing.Optional[Trie.TrieNode] = self._root
        if n is None:
            self._root = Trie.TrieNode()
            n = self._root
        assert n is not None, "unexpected error while performing __setitem__ on Trie"
        for c in key:
            if c not in n._children:
                n._children[c] = Trie.TrieNode()
            n = n._children[c]
        assert n is not None, "unexpected error while performing __setitem__ on Trie"
        n._value = value
        return self

    #
    # PUBLIC
    #
