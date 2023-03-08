#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains various implementations of `PageLayout`.
`PageLayout` can be used to add `LayoutElement` objects to a `Page` without
having to specify coordinates.
"""
import copy
import typing
from decimal import Decimal

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class MultiColumnLayout(PageLayout):
    """
    This implementation of PageLayout adds left/right/top/bottom margins to a Page
    and lays out the content on the Page as if there were multiple  columns to flow text, images, etc into.
    Once a column is full, the next column is automatically selected, although the next column can be manually selected.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        page: Page,
        number_of_columns: int = 2,
        horizontal_margin: typing.Optional[Decimal] = None,
        vertical_margin: typing.Optional[Decimal] = None,
        inter_column_margin: typing.Optional[Decimal] = None,
    ):
        super().__init__(page)

        # page width/height
        # fmt: off
        self._page_width: typing.Optional[Decimal] = self._page.get_page_info().get_width()
        self._page_height: typing.Optional[Decimal] = self._page.get_page_info().get_height()
        assert self._page_width, "page.get_width() must be defined for MultiColumnLayout to work"
        assert self._page_height, "page.get_height() must be defined for MultiColumnLayout to work"
        # fmt: on

        # horizontal margin
        self._inter_column_margin: Decimal = Decimal(self._page_width) * Decimal(0.05)
        if inter_column_margin is not None:
            self._inter_column_margin = inter_column_margin
        if horizontal_margin is None:
            self._horizontal_margin = self._page_width * Decimal(0.1)
        else:
            assert horizontal_margin >= 0
            self._horizontal_margin = horizontal_margin

        # vertical margin
        if vertical_margin is None:
            self._vertical_margin_top = self._page_height * Decimal(0.1)
            self._vertical_margin_bottom = self._vertical_margin_top
        else:
            assert vertical_margin >= 0
            self._vertical_margin_top = vertical_margin
            self._vertical_margin_bottom = vertical_margin

        self._number_of_columns = Decimal(number_of_columns)
        self._column_width = (
            self._page_width
            - Decimal(2) * self._horizontal_margin
            - Decimal(number_of_columns - 1) * self._inter_column_margin
        ) / Decimal(number_of_columns)

        # previous element information
        self._previous_element: typing.Optional[LayoutElement] = None
        self._current_column_index = Decimal(0)

    #
    # PRIVATE
    #

    def _get_margin_between_elements(
        self,
        previous_element: typing.Optional[LayoutElement],
        element: typing.Optional[LayoutElement],
    ) -> Decimal:
        if previous_element is None:
            return Decimal(0)
        if element is None:
            return Decimal(0)

        # text elements
        if isinstance(previous_element, ChunkOfText) and isinstance(
            element, ChunkOfText
        ):
            return max(
                previous_element.get_font_size() * Decimal(1.2),
                element.get_font_size() * Decimal(1.2),
            )
        if isinstance(previous_element, ChunkOfText):
            return previous_element.get_font_size() * Decimal(1.2)
        if isinstance(element, ChunkOfText):
            return element.get_font_size() * Decimal(1.2)

        # default
        return Decimal(5)

    #
    # PUBLIC
    #

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        """
        This method adds a `LayoutElement` to the current `Page`.
        """
        if self._current_column_index >= self._number_of_columns:
            return self

        # previous element is used to determine the paragraph spacing
        assert self._page_height is not None
        assert self._page_width is not None
        previous_element_margin_bottom: Decimal = Decimal(0)
        previous_element_y = self._page_height - self._vertical_margin_top
        if self._previous_element is not None:
            prev_element_prev_layout_box: typing.Optional[
                Rectangle
            ] = self._previous_element.get_previous_layout_box()
            assert prev_element_prev_layout_box is not None
            previous_element_y = prev_element_prev_layout_box.get_y()
            previous_element_margin_bottom = self._previous_element.get_margin_bottom()

        # calculate next available rectangle
        available_height: Decimal = (
            previous_element_y
            - self._vertical_margin_bottom
            - self._get_margin_between_elements(self._previous_element, layout_element)
            - max(previous_element_margin_bottom, layout_element.get_margin_top())
            - layout_element.get_margin_bottom()
        )

        # switch to new column if needed
        assert self._page_height
        if available_height < 0:
            self.switch_to_next_column()
            return self.add(layout_element)

        # fmt: off
        available_space: Rectangle = Rectangle(
            self._horizontal_margin + self._current_column_index * (self._column_width + self._inter_column_margin) + layout_element.get_margin_left(),
            self._vertical_margin_bottom + layout_element.get_margin_bottom(),
            self._column_width - layout_element.get_margin_right() - layout_element.get_margin_left(),
            available_height
        )
        # fmt: on

        # get layout_box
        layout_rect = layout_element.get_layout_box(available_space)
        if layout_rect.get_height() > available_space.get_height():
            if self._previous_element is not None:
                self.switch_to_next_column()
                return self.add(layout_element)
            else:
                assert False, (
                    "%s is too tall to fit inside column / page."
                    % layout_element.__class__.__name__
                )

        # content that is too large for the page should not be attempted to be laid out again
        if round(layout_rect.get_width(), 2) > round(self._column_width, 2):
            assert False, (
                "%s is too wide to fit inside column / page."
                % layout_element.__class__.__name__
            )

        # switch to next column
        if layout_rect.y < self._vertical_margin_bottom:
            self.switch_to_next_column()
            return self.add(layout_element)

        # paint
        layout_element.paint(self._page, available_space)

        # store previous
        self._previous_element = layout_element
        self._previous_element_layout_rect = layout_rect

        # return
        return self

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
        doc.add_page(new_page)

        # return
        return self


class SingleColumnLayout(MultiColumnLayout):
    """
    This implementation of PageLayout adds left/right/top/bottom margins to a Page
    and lays out the content on the Page as if there were was a single column to flow text, images, etc into.
    Once this column is full, the next page is automatically created.
    """

    #
    # CONSTRUCTOR
    #

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

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
