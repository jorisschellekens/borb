#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of MultiColumnLayout allows you to specify
a header and footer. In order to render the header and footer
you need to provide their maximum height(s) and a typing.Callable
which will do the actual rendering.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
from borb.pdf.page.page import Page


class HeaderFooterMultiColumnLayout(MultiColumnLayout):
    """
    This implementation of MultiColumnLayout allows you to specify
    a header and footer. In order to render the header and footer
    you need to provide their maximum height(s) and a typing.Callable
    which will do the actual rendering.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        # fmt: off
        self,
        page: Page,
        number_of_columns: int = 2,
        horizontal_margin: typing.Optional[Decimal] = None,
        vertical_margin: typing.Optional[Decimal] = None,
        header_callable: typing.Optional[typing.Callable[[Page, Rectangle], None]] = None,
        header_height: Decimal = Decimal(12 * 3 * 1.2),
        footer_height: Decimal = Decimal(12 * 3 * 1.2),
        footer_callable: typing.Optional[typing.Callable[[Page, Rectangle], None]] = None,
        inter_column_margin: typing.Optional[Decimal] = None,
        # fmt: on
    ):
        super(HeaderFooterMultiColumnLayout, self).__init__(
            page,
            number_of_columns,
            horizontal_margin,
            vertical_margin,
            inter_column_margin,
        )
        assert header_height >= 0
        assert footer_height >= 0
        self._header_height: Decimal = header_height
        self._footer_height: Decimal = footer_height
        self._header_callable = header_callable
        self._footer_callable = footer_callable

        if self._header_callable is None:
            self._header_height = Decimal(0)
        if self._footer_callable is None:
            self._footer_height = Decimal(0)

        # modify margins
        self._vertical_margin_bottom += self._footer_height
        self._vertical_margin_top += self._header_height

        # add header and footer to first Page
        self._add_header_footer_to_current_page()

    #
    # PRIVATE
    #

    def _add_header_footer_to_current_page(self) -> None:

        # add header
        if self._header_callable is not None:
            assert self._page_width is not None
            assert self._page_height is not None
            self._header_callable(
                self.get_page(),
                Rectangle(
                    self._horizontal_margin,
                    self._page_height - self._vertical_margin_top - self._header_height,
                    self._page_width - self._horizontal_margin * Decimal(2),
                    self._header_height,
                ),
            )

        # add footer
        assert self._page_width is not None
        assert self._page_height is not None
        if self._footer_callable is not None:
            self._footer_callable(
                self.get_page(),
                Rectangle(
                    self._horizontal_margin,
                    self._vertical_margin_bottom - self._footer_height,
                    self._page_width - self._horizontal_margin * Decimal(2),
                    self._footer_height,
                ),
            )

        # previous LayoutElement
        self._previous_element = ChunkOfText("")
        self._previous_element._previous_paint_box = Rectangle(
            self._horizontal_margin,
            self._page_height - self._vertical_margin_top - self._header_height,
            self._page_width - self._horizontal_margin * Decimal(2),
            self._header_height,
        )
        self._previous_element._previous_layout_box = (
            self._previous_element._previous_paint_box
        )

    #
    # PUBLIC
    #

    def switch_to_next_page(self) -> "PageLayout":  # type: ignore[name-defined]
        """
        This function forces this PageLayout to switch to the nex Page
        This function returns self.
        :return:    self
        """
        # call super
        super(HeaderFooterMultiColumnLayout, self).switch_to_next_page()

        # add header and footer to new page
        self._add_header_footer_to_current_page()

        # return
        return self
