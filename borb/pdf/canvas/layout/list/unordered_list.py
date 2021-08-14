#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an unordered list
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color, HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.list import List
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.page.page import Page


class UnorderedList(List):
    """
    This implementation of LayoutElement represents an unordered list
    """

    def __init__(
        self,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = HexColor("000000"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        margin_top: Decimal = None,
        margin_right: Decimal = None,
        margin_bottom: Decimal = None,
        margin_left: Decimal = None,
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,
    ):
        super(UnorderedList, self).__init__(
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
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
            parent=parent,
        )

    def _determine_level(self, layout_element: LayoutElement) -> int:
        level = 0
        e = layout_element
        while e._parent is not None:
            if isinstance(e, UnorderedList):
                level += 1
            e = e._parent
        return level

    def _get_bullet_text(self, item_index: int, item: LayoutElement) -> str:
        return ["●", "❍", "✦"][self._determine_level(item) % 3]

    def _get_bullet_layout_element(
        self, item_index: int, item: LayoutElement
    ) -> LayoutElement:
        if isinstance(item, List):
            return ChunkOfText(" ")
        return ChunkOfText(
            text=self._get_bullet_text(item_index, item),
            font_size=self.get_font_size(),
            font_color=X11Color("Black"),
            font="Zapfdingbats",
        )
