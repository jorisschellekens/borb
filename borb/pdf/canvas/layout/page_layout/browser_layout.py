#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of PageLayout attempts to mimic the way a web-browser
would display the LayoutElement objects (Paragraph, ChunkOfText, List, Table, etc)
"""
import typing
from decimal import Decimal
from enum import Enum

from borb.io.read.types import Name
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.horizontal_rule import HorizontalRule
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.table import Table
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class DisplayValue(Enum):
    """
    Every HTML element has a default display value, depending on what type of element it is.
    There are two display values: block and inline.
    -   A block-level element always starts on a new line.
        A block-level element always takes up the full width available (stretches out to the left and right as far as it can).
        A block level element has a top and a bottom margin, whereas an inline element does not.
    -   An inline element does not start on a new line.
        An inline element only takes up as much width as necessary.
    """

    INITIAL = 0
    BLOCK = 1
    INLINE = 2


class BrowserLayoutRow:
    """
    This class represents one row of LayoutElement objects that are being laid out.
    Grouping LayoutElement objects in rows can be useful when calculating their collective width,
    or their bounding box.
    """

    def __init__(self, display_value: DisplayValue):
        self._display_value = display_value
        self._layout_elements: typing.List[LayoutElement] = []

    def append(self, layout_element: LayoutElement) -> "BrowserLayoutRow":
        """
        This function appends a LayoutElement to this BrowserLayout.
        This function returns self.
        """
        self._layout_elements.append(layout_element)
        return self

    def get_display_value(self) -> DisplayValue:
        """
        This function returns the DisplayValue of this BrowserLayoutRow.
        """
        return self._display_value

    def get_bottom(self) -> Decimal:
        """
        This function returns the smallest y-value for any LayoutElement in this BrowserLayoutRow.
        """
        assert len(self._layout_elements) > 0
        return min([e.get_bounding_box().get_y() for e in self._layout_elements])  # type: ignore [union-attr]

    def get_margin_bottom(self) -> Decimal:
        """
        This function returns the bottom margin for the element with the smallest y-value in this BrowserLayout
        """
        if len(self._layout_elements) == 0:
            return Decimal(0)
        if self._display_value == DisplayValue.INLINE:
            return Decimal(0)
        return self._layout_elements[0].get_margin_bottom()

    def get_right(self):
        """
        This function returns the largest x-value for any LayoutElement in this BrowserLayoutRow
        """
        return max(
            [
                e.get_bounding_box().get_x() + e.get_bounding_box().get_width()
                for e in self._layout_elements
            ]
        )

    def get_margin_right(self):
        """
        This function returns the right margin for the element with the largest x-value in this BrowserLayout
        """
        if len(self._layout_elements) == 0:
            return Decimal(0)
        rightmost_element: typing.Optional[LayoutElement] = None
        for e in self._layout_elements:
            if rightmost_element is None:
                rightmost_element = e
                continue
            r0: Decimal = (
                e.get_bounding_box().get_x() + e.get_bounding_box().get_width()
            )
            r1: Decimal = (
                rightmost_element.get_bounding_box().get_x()
                + rightmost_element.get_bounding_box().get_width()
            )
            if r0 > r1:
                rightmost_element = e
        return rightmost_element.get_margin_right()

    def _align_ys(self) -> "BrowserLayoutRow":
        y: Decimal = self.get_bottom()
        for e in self._layout_elements:
            assert e.bounding_box is not None
            e.bounding_box.y = y
        return self

    def __len__(self):
        return len(self._layout_elements)


class BrowserLayout(PageLayout):
    """
    This implementation of PageLayout attempts to mimic the way a web-browser
    would display the LayoutElement objects (Paragraph, ChunkOfText, List, Table, etc)
    """

    def __init__(
        self,
        page: Page,
        horizontal_margin: typing.Optional[Decimal] = None,
        vertical_margin: typing.Optional[Decimal] = None,
    ):
        super(BrowserLayout, self).__init__(page)
        # page dimensions
        # fmt: off
        self._page_width: typing.Optional[Decimal] = self._page.get_page_info().get_width()
        assert self._page_width is not None
        self._page_height: typing.Optional[Decimal] = self._page.get_page_info().get_height()
        assert self._page_height is not None
        # fmt: on

        # page content
        self._page_content_stream_restore: bytes = b""
        if "Contents" in self._page and "DecodedBytes" in self._page["Contents"]:
            self._page_content_stream_restore = self._page["Contents"]["DecodedBytes"]

        # margins
        if horizontal_margin is None:
            self._horizontal_margin = self._page_width * Decimal(0.1)
        else:
            assert horizontal_margin >= 0
            self._horizontal_margin = horizontal_margin
        if vertical_margin is None:
            self._vertical_margin = self._page_height * Decimal(0.1)
        else:
            assert vertical_margin >= 0
            self._vertical_margin = vertical_margin

        # elements being laid out
        self._rows: typing.List[BrowserLayoutRow] = []

    def _get_initial_display_value(self, layout_element: LayoutElement) -> DisplayValue:
        #
        # BLOCK ELEMENTS
        #
        display_value: DisplayValue = DisplayValue.BLOCK
        if isinstance(layout_element, UnorderedList) or isinstance(
            layout_element, OrderedList
        ):
            display_value = DisplayValue.BLOCK
        elif isinstance(layout_element, Heading):
            display_value = DisplayValue.BLOCK
        elif isinstance(layout_element, HorizontalRule):
            display_value = DisplayValue.BLOCK
        elif isinstance(layout_element, Paragraph):
            display_value = DisplayValue.BLOCK
        elif isinstance(layout_element, Table):
            display_value = DisplayValue.BLOCK
        #
        # INLINE ELEMENTS
        #
        elif isinstance(layout_element, Image):
            display_value = DisplayValue.INLINE
        elif isinstance(layout_element, ChunkOfText):
            display_value = DisplayValue.INLINE
        #
        # DEFAULT
        #
        else:
            display_value = DisplayValue.BLOCK

        # return
        return display_value

    def _start_new_page(self):
        # get document
        pdf_document: Document = self._page.get_document()

        # create new Page
        page: Page = Page(self._page_width, self._page_height)
        pdf_document.append_page(page)

        # layout and reset rows
        self._page["Contents"][Name("DecodedBytes")] = self._page_content_stream_restore
        for e in self._rows[-1]._layout_elements:
            e.layout(self._page, e.get_bounding_box())  # type: ignore [arg-type]
        self._rows.clear()

        # reset layout
        self._page = page
        self._page_content_stream_restore = b""

    def _check_layout_element_dimensions(self, layout_element: LayoutElement) -> None:
        # content that is too large for the page should not be attempted to be laid out again
        layout_rect: typing.Optional[Rectangle] = layout_element.get_bounding_box()
        assert layout_rect is not None
        assert self._page_width is not None
        assert self._page_height is not None
        if round(layout_rect.get_width(), 2) > round(
            self._page_width - 2 * self._horizontal_margin, 2
        ):
            assert False, (
                "%s is too wide to fit inside column / page."
                % layout_element.__class__.__name__
            )
        if round(layout_rect.get_height(), 2) > round(
            self._page_height - 2 * self._vertical_margin, 2
        ):
            assert False, (
                "%s is too tall to fit inside column / page."
                % layout_element.__class__.__name__
            )

    def _add_block_element(self, layout_element: LayoutElement) -> None:
        assert self._page_width is not None
        assert self._page_height is not None
        prev_row_bottom: Decimal = self._page_height - self._vertical_margin
        prev_row_margin_bottom: Decimal = Decimal(0)
        if len(self._rows) > 0:
            prev_row_bottom = self._rows[-1].get_bottom()
            prev_row_margin_bottom = self._rows[-1].get_margin_bottom()

        # fmt: off
        x: Decimal = self._horizontal_margin + layout_element.get_margin_left()
        y: Decimal = self._vertical_margin + layout_element.get_margin_bottom()
        w: Decimal = self._page_width - Decimal(2) * self._horizontal_margin - layout_element.get_margin_right() - layout_element.get_margin_left()
        h: Decimal = prev_row_bottom - max(layout_element.get_margin_top(), prev_row_margin_bottom) - y
        # fmt: on

        # if height is negative --> new page
        if h < Decimal(0):
            self._start_new_page()
            self.add(layout_element, DisplayValue.BLOCK)
            return

        # catch potential layout problems as early as possible
        suggested_layout_box: Rectangle = layout_element._calculate_layout_box(
            self._page, Rectangle(x, y, w, h)
        )
        self._check_layout_element_dimensions(layout_element)

        # if the height + y exceeds the page height --> new page
        if suggested_layout_box.get_height() > h:
            self._start_new_page()
            self.add(layout_element, DisplayValue.BLOCK)
            return

        # else append to new row
        layout_element.layout(self._page, layout_element.get_bounding_box())  # type: ignore [arg-type]
        self._page_content_stream_restore = self._page["Contents"][Name("DecodedBytes")]
        self._rows.append(BrowserLayoutRow(DisplayValue.BLOCK).append(layout_element))

    def _add_inline_element(self, layout_element: LayoutElement) -> None:
        assert self._page_width is not None

        # set margins
        layout_element._margin_top = Decimal(0)
        layout_element._margin_bottom = Decimal(0)

        # append INLINE row (if needed)
        # fmt: off
        if len(self._rows) == 0:
            self._rows.append(BrowserLayoutRow(DisplayValue.INLINE))
        if len(self._rows) > 0 and self._rows[-1].get_display_value() == DisplayValue.BLOCK:
            self._rows.append(BrowserLayoutRow(DisplayValue.INLINE))
        # fmt: on

        assert self._page_height is not None
        prev_row_bottom: Decimal = self._page_height - self._vertical_margin
        prev_row_margin_bottom: Decimal = Decimal(0)
        if len(self._rows) > 1:
            prev_row_bottom = self._rows[-2].get_bottom()
            prev_row_margin_bottom = self._rows[-2].get_margin_bottom()

        # calculate leading
        # TODO
        leading: Decimal = Decimal(0)

        # fmt: off
        x: Decimal = self._horizontal_margin + layout_element.get_margin_left()
        if len(self._rows[-1]) > 0:
            x = self._rows[-1].get_right() + max(layout_element.get_margin_left(), self._rows[-1].get_margin_right())
        y: Decimal = self._vertical_margin + layout_element.get_margin_bottom()
        w: Decimal = self._page_width - self._horizontal_margin - layout_element.get_margin_right() - x
        h: Decimal = prev_row_bottom - max(layout_element.get_margin_top(), prev_row_margin_bottom) - y - leading
        # fmt: on

        # catch potential layout problems as early as possible
        suggested_layout_box: Rectangle = layout_element._calculate_layout_box(
            self._page, Rectangle(x, y, w, h)
        )
        self._check_layout_element_dimensions(layout_element)

        # if the height + y exceeds the page height --> new page
        if suggested_layout_box.get_height() > h:
            self._start_new_page()
            self.add(layout_element, DisplayValue.INLINE)
            return

        # if the width + y exceeds the page width --> new line
        if (
            suggested_layout_box.get_x()
            + suggested_layout_box.get_width()
            + layout_element.get_margin_right()
            > self._page_width - self._horizontal_margin
        ):

            # ensure page content is correct
            # fmt: off
            self._page["Contents"][Name("DecodedBytes")] = self._page_content_stream_restore
            for e in self._rows[-1]._layout_elements:
                e.layout(self._page, e.get_bounding_box())  # type: ignore [arg-type]
            self._page_content_stream_restore = self._page["Contents"][Name("DecodedBytes")]
            # fmt: on

            # append new row
            self._rows.append(BrowserLayoutRow(DisplayValue.INLINE))

            # try adding content again
            self.add(layout_element, DisplayValue.INLINE)
            return

        layout_element.layout(self._page, layout_element.get_bounding_box())  # type: ignore [arg-type]
        self._rows[-1].append(layout_element)
        self._rows[-1]._align_ys()

        # ensure page content is correct
        self._page["Contents"][Name("DecodedBytes")] = self._page_content_stream_restore
        for e in self._rows[-1]._layout_elements:
            e.layout(self._page, e.get_bounding_box())  # type: ignore [arg-type]

    def add(
        self,
        layout_element: LayoutElement,
        display_value: DisplayValue = DisplayValue.INITIAL,
    ) -> "PageLayout":
        """
        This method adds a `LayoutElement` to the current `Page`.
        """
        if display_value == DisplayValue.INITIAL:
            display_value = self._get_initial_display_value(layout_element)

        # block elements
        if display_value == DisplayValue.BLOCK:
            self._add_block_element(layout_element)
            return self

        # inline elements
        if display_value == DisplayValue.INLINE:
            self._add_inline_element(layout_element)
            return self

        # return
        return self
