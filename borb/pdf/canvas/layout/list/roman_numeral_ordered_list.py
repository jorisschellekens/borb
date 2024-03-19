#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an ordered (that is to say numbered) list.
For this list, roman numerals are used.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText


class RomanNumeralOrderedList(OrderedList):
    """
    This implementation of LayoutElement represents an ordered (that is to say numbered) list.
    For this list, roman numerals are used.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    def _get_bullet_layout_element(
        self, item_index: int, item: LayoutElement
    ) -> LayoutElement:
        # determine font_size from item
        font_size: Decimal = Decimal(12)
        try:
            font_size = item.get_font_size()
        except:
            pass

        # determine font_color from item
        font_color: Color = HexColor("000000")
        try:
            font_color = item.get_font_color()  # type: ignore[attr-defined]
        except:
            pass

        return ChunkOfText(
            text=self._int_to_roman(item_index + 1) + ".",
            font_size=font_size or Decimal(12),
            padding_right=Decimal(12),
            font_color=font_color or HexColor("000000"),
        )

    @staticmethod
    def _int_to_roman(value: int) -> str:
        """Convert an integer to a Roman numeral."""
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
