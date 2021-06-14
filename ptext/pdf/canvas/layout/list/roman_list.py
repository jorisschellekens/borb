#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an ordered (that is to say numbered) list.
For this list, roman numerals are used.
"""
from decimal import Decimal

from ptext.pdf.canvas.color.color import X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.list.ordered_list import OrderedList
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.page.page import Page


class RomanNumeralOrderedList(OrderedList):
    """
    This implementation of LayoutElement represents an ordered (that is to say numbered) list.
    For this list, roman numerals are used.
    """

    @staticmethod
    def _int_to_roman(value: int) -> str:
        """ Convert an integer to a Roman numeral. """
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

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:
        last_item_bottom: Decimal = bounding_box.y + bounding_box.height
        bullet_margin: Decimal = Decimal(20)
        for index, i in enumerate(self.items):
            # bullet character
            ChunkOfText(
                text=RomanNumeralOrderedList._int_to_roman(
                    index + 1 + self.index_offset
                )
                + ".",
                font_size=self._get_first_item_font_size(),
                font_color=X11Color("Black"),
            ).layout(
                page=page,
                bounding_box=Rectangle(
                    bounding_box.x,
                    bounding_box.y,
                    bullet_margin,
                    last_item_bottom - bounding_box.y,
                ),
            )
            # content
            item_rect = i.layout(
                page,
                bounding_box=Rectangle(
                    bounding_box.x + bullet_margin,
                    bounding_box.y,
                    bounding_box.width - bullet_margin,
                    last_item_bottom - bounding_box.y,
                ),
            )
            # set new last_item_bottom
            last_item_bottom = item_rect.y

        layout_rect = Rectangle(
            bounding_box.x,
            last_item_bottom,
            bounding_box.width,
            bounding_box.y + bounding_box.height - last_item_bottom,
        )

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
