#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains various implementations of `PageLayout`.
`PageLayout` can be used to add `LayoutElement` objects to a `Page` without
having to specify coordinates.
"""
import typing
import zlib
from decimal import Decimal

from borb.io.read.types import Decimal as pDecimal
from borb.io.read.types import Name
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page


class MultiColumnLayout(PageLayout):
    """
    This implementation of PageLayout adds left/right/top/bottom margins to a Page
    and lays out the content on the Page as if there were multiple  columns to flow text, images, etc into.
    Once a column is full, the next column is automatically selected, although the next column can be manually selected.
    """

    def __init__(
        self,
        page: Page,
        number_of_columns: int = 2,
        horizontal_margin: typing.Optional[Decimal] = None,
        vertical_margin: typing.Optional[Decimal] = None,
        fixed_paragraph_spacing: typing.Optional[Decimal] = None,
        multiplied_paragraph_spacing: typing.Optional[Decimal] = None,
    ):
        super().__init__(page)

        # page width/height
        # fmt: off
        self._page_width: typing.Optional[Decimal] = self._page.get_page_info().get_width()
        self._page_height: typing.Optional[Decimal] = self._page.get_page_info().get_height()
        assert self._page_width
        assert self._page_height
        # fmt: on

        # paragraph spacing
        if fixed_paragraph_spacing is None and multiplied_paragraph_spacing is None:
            multiplied_paragraph_spacing = Decimal(1.2)
        assert (
            fixed_paragraph_spacing is not None
            or multiplied_paragraph_spacing is not None
        )
        assert fixed_paragraph_spacing is None or fixed_paragraph_spacing >= 0
        assert multiplied_paragraph_spacing is None or multiplied_paragraph_spacing >= 0
        self._fixed_paragraph_spacing: typing.Optional[
            Decimal
        ] = fixed_paragraph_spacing
        self._multiplied_paragraph_spacing: typing.Optional[
            Decimal
        ] = multiplied_paragraph_spacing

        # horizontal margin
        if horizontal_margin is None:
            self._horizontal_margin = self._page_width * Decimal(0.1)
        else:
            assert horizontal_margin >= 0
            self._horizontal_margin = horizontal_margin

        # vertical margin
        if vertical_margin is None:
            self._vertical_margin = self._page_height * Decimal(0.1)
        else:
            assert vertical_margin >= 0
            self._vertical_margin = vertical_margin

        # inter-column margin
        self._inter_column_margin = self._page_width * Decimal(0.05)
        self._number_of_columns = Decimal(number_of_columns)
        self._column_width = (
            self._page_width
            - Decimal(2) * self._horizontal_margin
            - Decimal(number_of_columns - 1) * self._inter_column_margin
        ) / Decimal(number_of_columns)

        # previous element information
        self._previous_element: typing.Optional[LayoutElement] = None
        self._current_column_index = Decimal(0)

    def switch_to_next_column(self) -> "PageLayout":
        """
        This function forces this PageLayout to move to the next column on the Page
        """
        self._current_column_index += Decimal(1)
        if self._current_column_index == self._number_of_columns:
            return self.switch_to_next_page()
        assert self._page_height
        self._previous_element = None
        return self

    def switch_to_next_page(self) -> "PageLayout":
        """
        This function forces this PageLayout to move to the next Page
        """
        self._current_column_index = Decimal(0)
        assert self._page_height
        self._previous_element = None

        # find Document
        doc = self.get_page().get_root()  # type: ignore[attr-defined]
        assert isinstance(doc, Document)

        # create new Page
        assert self._page_width
        assert self._page_height
        new_page = Page(width=self._page_width, height=self._page_height)
        self._page = new_page
        doc.append_page(new_page)

        # return
        return self

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        """
        This method adds a `LayoutElement` to the current `Page`.
        """
        if self._current_column_index >= self._number_of_columns:
            return self

        # previous element is used to determine the paragraph spacing
        previous_element_margin_bottom: Decimal = Decimal(0)
        previous_element_y = self._page_height - self._vertical_margin
        inter_paragraph_space: Decimal = Decimal(0)
        if self._previous_element is not None:
            previous_element_margin_bottom = self._previous_element.get_margin_bottom()
            previous_element_y = self._previous_element.get_bounding_box().get_y()

            # generate space
            if isinstance(self._previous_element, Paragraph) or isinstance(
                layout_element, Paragraph
            ):
                assert (
                    self._multiplied_paragraph_spacing is not None
                    or self._fixed_paragraph_spacing is not None
                )
                assert (
                    self._multiplied_paragraph_spacing is None
                    or self._multiplied_paragraph_spacing > 0
                )
                assert (
                    self._fixed_paragraph_spacing is None
                    or self._fixed_paragraph_spacing > 0
                )
                if self._multiplied_paragraph_spacing is not None:
                    inter_paragraph_space = (
                        layout_element.get_font_size()
                        * self._multiplied_paragraph_spacing
                    )
                if self._fixed_paragraph_spacing is not None:
                    inter_paragraph_space = self._fixed_paragraph_spacing

        # calculate next available rectangle
        available_height: Decimal = (
            previous_element_y
            - self._vertical_margin
            - inter_paragraph_space
            - max(previous_element_margin_bottom, layout_element.get_margin_top())
            - layout_element.get_margin_bottom()
        )
        assert self._page_height
        if available_height < 0:
            self.switch_to_next_column()
            return self.add(layout_element)

        # fmt: off
        next_available_rect: Rectangle = Rectangle(
            self._horizontal_margin + self._current_column_index * (self._column_width + self._inter_column_margin) + layout_element.get_margin_left(),
            self._vertical_margin + layout_element.get_margin_bottom(),
            self._column_width - layout_element.get_margin_right() - layout_element.get_margin_left(),
            available_height
        )
        # fmt: on

        # store previous contents
        if "Contents" not in self._page:
            layout_element._initialize_page_content_stream(self._page)
        previous_decoded_bytes = self._page["Contents"]["DecodedBytes"]

        # attempt layout
        layout_rect = layout_element.layout(
            self._page, bounding_box=next_available_rect
        )

        # content that is too large for the page should not be attempted to be laid out again
        if round(layout_rect.get_width(), 2) > round(self._column_width, 2):
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

        # switch to next column
        if layout_rect.y < self._vertical_margin:
            content_stream = self._page["Contents"]
            content_stream[Name("DecodedBytes")] = previous_decoded_bytes
            content_stream[Name("Bytes")] = zlib.compress(
                content_stream["DecodedBytes"], 9
            )
            content_stream[Name("Length")] = pDecimal(len(content_stream["Bytes"]))
            self.switch_to_next_column()
            return self.add(layout_element)

        # calculate previous_y
        self._previous_element = layout_element

        # return
        return self


class SingleColumnLayout(MultiColumnLayout):
    """
    This implementation of PageLayout adds left/right/top/bottom margins to a Page
    and lays out the content on the Page as if there were was a single column to flow text, images, etc into.
    Once this column is full, the next page is automatically created.
    """

    def __init__(
        self,
        page: Page,
        horizontal_margin: typing.Optional[Decimal] = None,
        vertical_margin: typing.Optional[Decimal] = None,
    ):
        super(SingleColumnLayout, self).__init__(
            page,
            number_of_columns=1,
            horizontal_margin=horizontal_margin,
            vertical_margin=vertical_margin,
        )
        self._inter_column_margin = Decimal(0)
