#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of MultiColumnLayout allows you to specify
a header and footer. In order to render the header and footer
you need to provide their maximum height(s) and a typing.Callable
which will do the actual rendering.
"""
import typing
import zlib
from decimal import Decimal

from borb.io.read.types import Name, Decimal as bDecimal
from borb.pdf import Paragraph
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout


class HeaderFooterMultiColumnLayout(MultiColumnLayout):
    """
    This implementation of MultiColumnLayout allows you to specify
    a header and footer. In order to render the header and footer
    you need to provide their maximum height(s) and a typing.Callable
    which will do the actual rendering.
    """

    def __init__(
        self,
        page: Page,
        number_of_columns: int = 2,
        horizontal_margin: typing.Optional[Decimal] = None,
        vertical_margin: typing.Optional[Decimal] = None,
        header_callable: typing.Optional[
            typing.Callable[[Page, Rectangle], None]
        ] = None,
        header_height: typing.Optional[Decimal] = None,
        footer_height: typing.Optional[Decimal] = None,
        footer_callable: typing.Optional[
            typing.Callable[[Page, Rectangle], None]
        ] = None,
        fixed_paragraph_spacing: typing.Optional[Decimal] = None,
        multiplied_paragraph_spacing: typing.Optional[Decimal] = None,
        multiplied_inter_column_spacing: typing.Optional[Decimal] = None,
    ):
        super(HeaderFooterMultiColumnLayout, self).__init__(
            page,
            number_of_columns,
            horizontal_margin,
            vertical_margin,
            fixed_paragraph_spacing,
            multiplied_paragraph_spacing,
            multiplied_inter_column_spacing,
        )
        assert (header_height is None) or (header_height >= 0)
        assert (footer_height is None) or (footer_height >= 0)
        # fmt: off
        self._header_height: Decimal = Decimal(0)
        self._footer_height: Decimal = Decimal(0)
        if header_callable is not None:
            self._header_height = header_height or Decimal(42)  # 42 is roughly equal to 3 lines of text, in Helvetica 12, with default leading
        if footer_callable is not None:
            self._footer_height = footer_height or Decimal(42)  # 42 is roughly equal to 3 lines of text, in Helvetica 12, with default leading
        # fmt: on
        self._header_callable = header_callable
        self._footer_callable = footer_callable

        # size of Page is updated to ensure the layout algorithm does not attempt
        # to fill the Page entirely
        self._page_height -= header_height or Decimal(0)
        self._page_height -= footer_height or Decimal(0)

        # add header and footer to first Page
        self._add_header_footer_to_current_page()

    def _add_header_footer_to_current_page(self) -> None:

        # add header
        if self._header_callable is not None:
            self._header_callable(
                self.get_page(),
                Rectangle(
                    self._horizontal_margin,
                    self._page_height - self._header_height - self._vertical_margin,
                    self._page_width - self._horizontal_margin * Decimal(2),
                    self._header_height,
                ),
            )

        # add footer
        if self._footer_callable is not None:
            self._footer_callable(
                self.get_page(),
                Rectangle(
                    self._horizontal_margin,
                    self._vertical_margin,
                    self._page_width - self._horizontal_margin * Decimal(2),
                    self._footer_height,
                ),
            )

    def switch_to_next_page(self) -> "PageLayout":
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
        previous_element_y = (
            self._page_height - self._vertical_margin - self._header_height
        )
        inter_paragraph_space: Decimal = Decimal(0)
        if self._previous_element is not None:
            previous_element_margin_bottom = self._previous_element.get_margin_bottom()
            previous_element_y = self._previous_element.get_bounding_box().get_y()

            # generate space
            if isinstance(self._previous_element, Paragraph) or isinstance(
                layout_element, Paragraph
            ):
                # fmt: off
                assert self._multiplied_paragraph_spacing is not None or self._fixed_paragraph_spacing is not None
                assert self._multiplied_paragraph_spacing is None or self._multiplied_paragraph_spacing > 0
                assert self._fixed_paragraph_spacing is None or self._fixed_paragraph_spacing > 0
                # fmt: on
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
            - self._footer_height
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
            self._horizontal_margin + self._current_column_index * (self._column_width + self._inter_column_spacing) + layout_element.get_margin_left(),
            self._vertical_margin + self._footer_height + layout_element.get_margin_bottom(),
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
            self._page_height
            - 2 * self._vertical_margin
            - self._header_height
            - self._footer_height,
            2,
        ):
            assert False, (
                "%s is too tall to fit inside column / page."
                % layout_element.__class__.__name__
            )

        # switch to next column
        lowest_allowed_y: Decimal = self._footer_height + self._vertical_margin
        if layout_rect.y < lowest_allowed_y:
            # fmt: off
            content_stream = self._page["Contents"]
            content_stream[Name("DecodedBytes")] = previous_decoded_bytes
            content_stream[Name("Bytes")] = zlib.compress(content_stream["DecodedBytes"], 9)
            content_stream[Name("Length")] = bDecimal(len(content_stream["Bytes"]))
            self.switch_to_next_column()
            return self.add(layout_element)
            # fmt: on

        # calculate previous_y
        self._previous_element = layout_element

        # return
        return self
