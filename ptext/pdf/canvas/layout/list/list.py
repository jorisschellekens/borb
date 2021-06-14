#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains implementation of LayoutElement representing lists (ordered and unordered)
"""
import typing
from decimal import Decimal

from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.layout.layout_element import LayoutElement
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText


class List(LayoutElement):
    """
    This implementation of LayoutElement represents a list
    """

    def __init__(
        self,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_color: Color = X11Color("Black"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        background_color: typing.Optional[Color] = None,
        parent: typing.Optional["LayoutElement"] = None,
    ):
        super(List, self).__init__(
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
            background_color=background_color,
            parent=parent,
        )
        self.parent = parent
        self.items: typing.List[LayoutElement] = []

    def _get_first_item_font_size(self) -> Decimal:
        for i in self.items:
            # copy font_size of text elements
            if isinstance(i, ChunkOfText):
                return i.font_size
        for i in self.items:
            # nested lists
            if isinstance(i, List):
                return i._get_first_item_font_size()
        return Decimal(12)

    def add(self, element: LayoutElement) -> "List":
        """
        This function adds a LayoutElement to this List
        """
        self.items.append(element)
        element.parent = self
        return self
