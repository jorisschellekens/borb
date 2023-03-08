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
        self._bullet_margin: Decimal = Decimal(20)
        self._items: typing.List[LayoutElement] = []

    #
    # PRIVATE
    #

    def _get_bullet_layout_element(
        self, item_index: int, item: LayoutElement
    ) -> LayoutElement:
        return ChunkOfText(
            text="●",
            font_size=self.get_font_size(),
            font_color=X11Color("Black"),
            font="Zapfdingbats",
        )

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        previous_layout_box: typing.Optional[Rectangle] = None
        min_x: typing.Optional[Decimal] = None
        min_y: typing.Optional[Decimal] = None
        max_x: typing.Optional[Decimal] = None
        max_y: typing.Optional[Decimal] = None
        for index, e in enumerate(self._items):
            if previous_layout_box is None:
                previous_layout_box = e.get_layout_box(
                    Rectangle(
                        available_space.get_x() + self._bullet_margin,
                        available_space.get_y(),
                        available_space.get_width() - self._bullet_margin,
                        available_space.get_height(),
                    )
                )
            else:
                previous_layout_box = e.get_layout_box(
                    Rectangle(
                        available_space.get_x() + self._bullet_margin,
                        available_space.get_y(),
                        available_space.get_width() - self._bullet_margin,
                        max(
                            Decimal(0),
                            previous_layout_box.get_y() - available_space.get_y(),
                        ),
                    )
                )

            # update min_x
            assert previous_layout_box is not None
            min_x = (
                previous_layout_box.get_x()
                if min_x is None
                else min(min_x, previous_layout_box.get_x())
            )
            min_y = (
                previous_layout_box.get_y()
                if min_y is None
                else min(min_y, previous_layout_box.get_y())
            )
            max_x = (
                previous_layout_box.get_x() + previous_layout_box.get_width()
                if max_x is None
                else max(
                    max_x, previous_layout_box.get_x() + previous_layout_box.get_width()
                )
            )
            max_y = (
                previous_layout_box.get_y() + previous_layout_box.get_height()
                if max_y is None
                else max(
                    max_y,
                    previous_layout_box.get_y() + previous_layout_box.get_height(),
                )
            )

        # return
        assert min_x is not None
        assert min_y is not None
        assert max_x is not None
        assert max_y is not None
        return Rectangle(
            min_x - self._bullet_margin,
            min_y,
            max_x - min_x + self._bullet_margin,
            max_y - min_y,
        )

    def _paint_content_box(self, page: "Page", available_space: Rectangle) -> None:
        previous_layout_box: typing.Optional[Rectangle] = None
        for index, e in enumerate(self._items):
            if previous_layout_box is None:
                previous_layout_box = e.get_layout_box(
                    Rectangle(
                        available_space.get_x() + self._bullet_margin,
                        available_space.get_y(),
                        available_space.get_width() - self._bullet_margin,
                        available_space.get_height(),
                    )
                )
            else:
                previous_layout_box = e.get_layout_box(
                    Rectangle(
                        available_space.get_x() + self._bullet_margin,
                        available_space.get_y(),
                        available_space.get_width() - self._bullet_margin,
                        previous_layout_box.get_y() - available_space.get_y(),
                    )
                )
            # paint item
            assert previous_layout_box is not None
            e.paint(page, previous_layout_box)

            # paint bullet
            self._get_bullet_layout_element(index, e).paint(
                page,
                Rectangle(
                    available_space.get_x(),
                    previous_layout_box.get_y(),
                    self._bullet_margin,
                    previous_layout_box.get_height(),
                ),
            )

    #
    # PUBLIC
    #

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
