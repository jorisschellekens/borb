#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an ordered (that is to say numbered) list
"""
import typing
from decimal import Decimal

from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.layout_element import LayoutElement
from ptext.pdf.canvas.layout.list.list import List
from ptext.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from ptext.pdf.page.page import Page


class OrderedList(List):
    """
    This implementation of LayoutElement represents an ordered (that is to say numbered) list
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
        super(OrderedList, self).__init__(
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
        self.index_offset = 0
        self.items: typing.List[LayoutElement] = []

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:
        last_item_bottom: Decimal = bounding_box.y + bounding_box.height
        bullet_margin: Decimal = Decimal(20)
        for index, i in enumerate(self.items):
            # bullet character
            ChunkOfText(
                text=str(index + 1 + self.index_offset) + ".",
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
