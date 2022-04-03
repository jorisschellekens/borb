#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains implementation of LayoutElement representing lists (ordered and unordered)
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color, HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement, Alignment
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.page.page import Page


class List(LayoutElement):
    """
    This implementation of LayoutElement represents a list
    """

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
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        super(List, self).__init__(
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            font_size=Decimal(12),
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        self._items: typing.List[LayoutElement] = []

    def add(self, element: LayoutElement) -> "List":
        """
        This function adds a LayoutElement to this List
        """
        if self._font_size is None:
            self._font_size = element.get_font_size()
        if self._margin_top is None:
            self._margin_top = element.get_font_size()
        if self._margin_bottom is None:
            self._margin_bottom = element.get_font_size()
        self._items.append(element)
        element._parent = self
        return self

    def _get_bullet_layout_element(
        self, item_index: int, item: LayoutElement
    ) -> LayoutElement:
        return ChunkOfText(
            text="●",
            font_size=self.get_font_size(),
            font_color=X11Color("Black"),
            font="Zapfdingbats",
        )

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # calculate the height of each item
        bullet_margin: Decimal = Decimal(20)
        for i in self._items:
            i._calculate_layout_box(
                page,
                bounding_box=Rectangle(
                    bounding_box.x + i.get_margin_left() + bullet_margin,
                    bounding_box.y + i.get_margin_bottom(),
                    bounding_box.width
                    - bullet_margin
                    - i.get_margin_right()
                    - i.get_margin_left(),
                    bounding_box.height - i.get_margin_top(),
                ),
            )

        for index, item in enumerate(self._items):
            # item bounding box
            item_bounding_box: typing.Optional[Rectangle] = item.get_bounding_box()
            assert item_bounding_box is not None

            # calculate previous (item) bottom
            # fmt: off
            previous_item_bottom: Decimal = (bounding_box.y + bounding_box.height - item.get_margin_top())
            if index > 0:
                previous_item: LayoutElement = self._items[index - 1]
                previous_item_bounding_box: typing.Optional[Rectangle] = previous_item.get_bounding_box()
                assert previous_item_bounding_box is not None
                previous_item_bottom = previous_item_bounding_box.get_y() - max(previous_item.get_margin_bottom(), item.get_margin_top())
            item_height: Decimal = item_bounding_box.get_height()
            # fmt: on

            # bullet character
            self._get_bullet_layout_element(index, item).layout(
                page=page,
                bounding_box=Rectangle(
                    bounding_box.x,
                    previous_item_bottom - item_height,
                    bullet_margin,
                    item_height,
                ),
            )
            # content
            item.layout(
                page,
                bounding_box=Rectangle(
                    bounding_box.x + bullet_margin + item.get_margin_left(),
                    previous_item_bottom - item_height,
                    bounding_box.width
                    - bullet_margin
                    - item.get_margin_right()
                    - item.get_margin_left(),
                    item_height,
                ),
            )

        # fmt: off
        layout_rect = Rectangle(
            bounding_box.x,
            self._items[-1].get_bounding_box().get_y() - self._items[-1].get_margin_bottom(),                                           # type: ignore [union-attr]
            bounding_box.width,
            bounding_box.y + bounding_box.height - self._items[-1].get_bounding_box().get_y() + self._items[-1].get_margin_bottom(),    # type: ignore [union-attr]
        )
        # fmt: on

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
