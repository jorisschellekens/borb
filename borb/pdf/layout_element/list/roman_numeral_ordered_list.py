#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an ordered list of layout elements numbered with Roman numerals.

The `RomanNumeralOrderedList` class is designed to manage a list of layout elements
that are numbered using Roman numerals (I, II, III, etc.) instead of Arabic numerals.
Each item in the list is automatically assigned a Roman numeral index based on its
position in the list. This class extends the functionality of a basic ordered list
to provide customized numbering.
"""

from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.ordered_list import OrderedList
from borb.pdf.layout_element.text.chunk import Chunk


class RomanNumeralOrderedList(OrderedList):
    """
    Represents an ordered list of layout elements numbered with Roman numerals.

    The `RomanNumeralOrderedList` class is designed to manage a list of layout elements
    that are numbered using Roman numerals (I, II, III, etc.) instead of Arabic numerals.
    Each item in the list is automatically assigned a Roman numeral index based on its
    position in the list. This class extends the functionality of a basic ordered list
    to provide customized numbering.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __int_to_roman(value: int) -> str:
        """
        Convert an integer to its Roman numeral representation.

        This function takes an integer and converts it into a Roman numeral string.
        It handles values typically from 1 to 3999, which are the common range for Roman numerals.

        :param value:   The integer to be converted
        :return:        The roman numeral representation
        """
        assert value > 0, "_int_to_roman can only convert values from 1 to 3999"
        assert value < 4000, "_int_to_roman can only convert values from 1 to 3999"
        ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
        nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
        result = []
        for i in range(len(ints)):
            count = int(value / ints[i])
            result.append(nums[i] * count)
            value -= ints[i] * count
        return "".join(result)

    #
    # PUBLIC
    #

    def append_layout_element(
        self, layout_element: LayoutElement
    ) -> "RomanNumeralOrderedList":
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
        self._OrderedList__index_items.append(Chunk(text=f"{RomanNumeralOrderedList.__int_to_roman(n)}."))  # type: ignore[attr-defined]

        # return
        return self
