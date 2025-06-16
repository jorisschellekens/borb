#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an alphabetically ordered list of layout elements.

The `ABCOrderedList` class arranges items in a list using an alphabetical
ordering scheme, starting from 'a', 'b', 'c', and continuing through
'z', then 'aa', 'ab', etc. This class is particularly useful for managing
ordered lists in documents where items need to be presented in a sequential,
lettered format.
"""
import typing

from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.ordered_list import OrderedList
from borb.pdf.layout_element.text.chunk import Chunk


class ABCOrderedList(OrderedList):
    """
    Represents an alphabetically ordered list of layout elements.

    The `ABCOrderedList` class arranges items in a list using an alphabetical
    ordering scheme, starting from 'a', 'b', 'c', and continuing through
    'z', then 'aa', 'ab', etc. This class is particularly useful for managing
    ordered lists in documents where items need to be presented in a sequential,
    lettered format.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __int_to_abc(value: int) -> str:
        """
        Convert an integer to a corresponding alphabetic label (a, b, ..., z, aa, ab, etc.).

        This function takes an integer and converts it into its alphabetic representation,
        following the pattern of Excel column labels. For example, the input 1 returns 'a',
        2 returns 'b', and 27 returns 'aa'.

        :param value:   The integer to be converted.
        :return:        The alphabetic representation of the integer.
        """
        result: typing.List[str] = []
        while value > 0:
            value -= 1  # Adjust for 0-based indexing
            result.append(chr(value % 26 + ord("a")))
            value //= 26
        return "".join(reversed(result))

    #
    # PUBLIC
    #

    def append_layout_element(self, layout_element: LayoutElement) -> "ABCOrderedList":
        """
        Add a layout element to the list and update the index.

        This method adds a layout element (such as a text block, image, or another element)
        to the ordered list and updates the list's index by appending a new index item
        (e.g., a numbered label). The index for the newly added item is automatically
        incremented and formatted as a numbered chunk.

        :param layout_element:   The LayoutElement to be added.
        :return:    Self, to allow for method chaining.
        """
        self._List__list_items.append(layout_element)  # type: ignore[attr-defined]

        # add Chunk as index item
        n: int = len(self._List__list_items)  # type: ignore[attr-defined]
        self._OrderedList__index_items.append(Chunk(text=f"{ABCOrderedList.__int_to_abc(n)}."))  # type: ignore[attr-defined]

        # return
        return self
