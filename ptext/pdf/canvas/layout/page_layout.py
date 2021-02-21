#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains various implementations of `PageLayout`.
    `PageLayout` can be used to add `LayoutElement` objects to a `Page` without
    having to specify coordinates.
"""
import zlib

from ptext.io.read.types import Decimal, Name
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import (
    LayoutElement,
    ChunkOfText,
    LineOfText,
    Paragraph,
)
from ptext.pdf.page.page import Page


class PageLayout:
    """
    This class acts as a layoutmanager for `Document` objects.
    Instead of adding `LayoutElements` to a `Page` by calling `layout` (and needing to know the precise coordinates)
    you can simply use this class and its `add` method.
    Any implementation of `PageLayout` should keep track of where `LayoutElement` objects are placed,
    and what the remaining free space is.
    """

    def __init__(self, page: Page):
        self.page = page

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        """
        This method adds a `LayoutElement` to the current `Page`.
        The specific implementation of `PageLayout` should decide where the `LayoutElement` will be placed.
        """
        return self


class SingleColumnLayout(PageLayout):
    def __init__(self, page: Page):
        super().__init__(page)

        self.page_width = self.page.get_page_info().get_width()
        self.page_height = self.page.get_page_info().get_height()

        assert self.page_width
        assert self.page_height

        self.horizontal_margin = self.page_width * Decimal(0.1)
        self.vertical_margin = self.page_height * Decimal(0.1)

        self.previous_y = self.page_height - self.vertical_margin
        self.previous_leading = Decimal(0)

    def add(self, layout_element: LayoutElement):
        # calculate next available rectangle
        assert self.page_width
        next_available_rect: Rectangle = Rectangle(
            self.horizontal_margin,
            self.vertical_margin,
            self.page_width - Decimal(2) * self.horizontal_margin,
            self.previous_y - self.vertical_margin - self.previous_leading,
        )
        # layout
        layout_rect = layout_element.layout(self.page, next_available_rect)

        # calculate previous_y
        self.previous_y = layout_rect.y
        self.previous_leading = self._calculate_leading(layout_element)

        # return
        return self

    def _calculate_leading(self, layout_element: LayoutElement) -> Decimal:
        if isinstance(layout_element, ChunkOfText):
            return layout_element.font_size * Decimal(1.3)
        if isinstance(layout_element, LineOfText):
            return layout_element.font_size * Decimal(1.3)
        if isinstance(layout_element, Paragraph):
            return layout_element.font_size * Decimal(1.3)
        # fixed leading
        return Decimal(12)


class MultiColumnLayout(PageLayout):
    def __init__(self, page: Page, number_of_columns: int = 2):
        super().__init__(page)

        self.page_width = self.page.get_page_info().get_width()
        self.page_height = self.page.get_page_info().get_height()

        assert self.page_width
        assert self.page_height

        self.horizontal_margin = self.page_width * Decimal(0.1)
        self.vertical_margin = self.page_height * Decimal(0.1)
        self.inter_column_margin = self.page_width * Decimal(0.05)
        self.number_of_columns = Decimal(number_of_columns)
        self.column_width = (
            self.page_width
            - Decimal(2) * self.horizontal_margin
            - Decimal(number_of_columns - 1) * self.inter_column_margin
        ) / Decimal(number_of_columns)

        self.previous_y = self.page_height - self.vertical_margin
        self.previous_leading = Decimal(0)
        self.column_index = Decimal(0)

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        if self.column_index >= self.number_of_columns:
            return self

        # calculate next available rectangle
        available_height: Decimal = (
            self.previous_y - self.vertical_margin - self.previous_leading
        )
        assert self.page_height
        if available_height < 0:
            self.column_index += Decimal(1)
            self.previous_y = self.page_height - self.vertical_margin
            self.previous_leading = Decimal(0)
            return self.add(layout_element)

        next_available_rect: Rectangle = Rectangle(
            self.horizontal_margin
            + self.column_index * (self.column_width + self.inter_column_margin),
            self.vertical_margin,
            self.column_width,
            self.previous_y - self.vertical_margin - self.previous_leading,
        )

        # store previous contents
        if "Contents" not in self.page:
            layout_element._initialize_page_content_stream(self.page)
        previous_decoded_bytes = self.page["Contents"]["DecodedBytes"]

        # attempt layout
        layout_rect = layout_element.layout(self.page, bounding_box=next_available_rect)
        if layout_rect.y < self.vertical_margin:
            content_stream = self.page["Contents"]
            content_stream["DecodedBytes"] = previous_decoded_bytes
            content_stream[Name("Bytes")] = zlib.compress(
                content_stream["DecodedBytes"], 9
            )
            content_stream[Name("Length")] = Decimal(len(content_stream["Bytes"]))
            self.column_index += Decimal(1)
            self.previous_y = self.page_height - self.vertical_margin
            self.previous_leading = Decimal(0)
            self.add(layout_element)
            return self

        # calculate previous_y
        self.previous_y = layout_rect.y
        self.previous_leading = self._calculate_leading(layout_element)

        # return
        return self

    def _calculate_leading(self, layout_element: LayoutElement) -> Decimal:
        if isinstance(layout_element, ChunkOfText):
            return layout_element.font_size * Decimal(1.3)
        if isinstance(layout_element, LineOfText):
            return layout_element.font_size * Decimal(1.3)
        if isinstance(layout_element, Paragraph):
            return layout_element.font_size * Decimal(1.3)
        # fixed leading
        return Decimal(12)
