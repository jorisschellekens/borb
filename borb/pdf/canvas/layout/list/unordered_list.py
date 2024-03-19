#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an unordered list
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.list import List
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText


class UnorderedList(List):
    """
    This implementation of LayoutElement represents an unordered list
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
        super(UnorderedList, self).__init__(
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

    def _determine_level(self, layout_element: LayoutElement) -> int:
        level = 0
        e = layout_element
        while e._parent is not None:
            if isinstance(e, UnorderedList):
                level += 1
            e = e._parent
        return level

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

        # nested List objects
        if isinstance(item, List):
            return ChunkOfText(" ", font_size=font_size, padding_right=Decimal(12))

        # default
        return ChunkOfText(
            text=self._get_bullet_text(item_index, item),
            font_size=font_size or Decimal(12),
            padding_right=Decimal(12),
            font_color=font_color or HexColor("000000"),
            font="ZapfDingbats",
            vertical_alignment=Alignment.TOP,
        )

    def _get_bullet_text(self, item_index: int, item: LayoutElement) -> str:
        return ["●", "❍", "✦"][self._determine_level(item) % 3]

    #
    # PUBLIC
    #
