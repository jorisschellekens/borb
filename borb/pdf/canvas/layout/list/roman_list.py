#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an ordered (that is to say numbered) list.
For this list, roman numerals are used.
"""

from borb.pdf.canvas.color.color import X11Color
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText


class RomanNumeralOrderedList(OrderedList):
    """
    This implementation of LayoutElement represents an ordered (that is to say numbered) list.
    For this list, roman numerals are used.
    """

    @staticmethod
    def _int_to_roman(value: int) -> str:
        """Convert an integer to a Roman numeral."""
        assert value > 0
        assert value < 4000
        ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
        nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
        result = []
        for i in range(len(ints)):
            count = int(value / ints[i])
            result.append(nums[i] * count)
            value -= ints[i] * count
        return "".join(result)

    def _get_bullet_layout_element(
        self, item_index: int, item: LayoutElement
    ) -> LayoutElement:
        return ChunkOfText(
            text=self._int_to_roman(item_index + 1) + ".",
            font_size=self.get_font_size(),
            font_color=X11Color("Black"),
        )
