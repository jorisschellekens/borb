#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an ordered (that is to say numbered) list
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.list import List
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText


class OrderedList(List):
    """
    This implementation of LayoutElement represents an ordered (that is to say numbered) list
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: Decimal = None,
        margin_left: Decimal = None,
        margin_right: Decimal = None,
        margin_top: Decimal = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(OrderedList, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_bottom_left=border_radius_bottom_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            background_color=background_color,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
        )

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
            if font_size == Decimal(0):
                font_size = Decimal(12)
        except:
            pass

        # determine font_color from item
        font_color: Color = HexColor("000000")
        try:
            font_color = item.get_font_color()  # type: ignore[attr-defined]
        except:
            pass

        # return
        return ChunkOfText(
            text=str(item_index + 1) + ".",
            font_size=font_size,
            padding_right=Decimal(12),
            font_color=font_color,
            horizontal_alignment=Alignment.RIGHT,
        )

    #
    # PUBLIC
    #
