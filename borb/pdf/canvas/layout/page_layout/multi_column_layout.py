#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains various implementations of `PageLayout`.
`PageLayout` can be used to add `LayoutElement` objects to a `Page` without
having to specify coordinates.
"""
import logging
import typing
from decimal import Decimal

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout

logger = logging.getLogger(__name__)


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
        page: "Page",  # type: ignore[name-defined]
        column_widths: typing.List[Decimal] = [],
        footer_paint_method: typing.Optional[typing.Callable[["Page", Rectangle], None]] = None,  # type: ignore[name-defined]
        header_paint_method: typing.Optional[typing.Callable[["Page", Rectangle], None]] = None,  # type: ignore[name-defined]
        inter_column_margins: typing.List[Decimal] = [],
        margin_bottom: Decimal = Decimal(84.2),
        margin_left: Decimal = Decimal(59.5),
        margin_right: Decimal = Decimal(59.5),
        margin_top: Decimal = Decimal(84.2),
    ):
        # check
        assert margin_top >= 0
        assert margin_right >= 0
        assert margin_bottom >= 0
        assert margin_left >= 0
        assert len(column_widths) >= 1
        assert len(inter_column_margins) + 1 == len(column_widths)

        # init
        super().__init__(page)
        self._column_widths: typing.List[Decimal] = column_widths
        self._inter_column_margins: typing.List[Decimal] = inter_column_margins
        self._footer_paint_method: typing.Optional[typing.Callable[["Page", Rectangle], None]] = footer_paint_method  # type: ignore[name-defined]
        self._header_paint_method: typing.Optional[typing.Callable[["Page", Rectangle], None]] = header_paint_method  # type: ignore[name-defined]
        self._margin_bottom: Decimal = margin_bottom
        self._margin_left: Decimal = margin_left
        self._margin_right: Decimal = margin_right
        self._margin_top = margin_top
        self._previous_layout_element: typing.Optional[LayoutElement] = None

        # keeping track of columns
        self._number_of_columns: int = len(column_widths)
        self._active_column: int = 0

        # add header/footer
        self._add_header_and_footer()

    #
    # PRIVATE
    #

    def _add_header_and_footer(self) -> "PageLayout":
        w: typing.Optional[Decimal] = self._page.get_page_info().get_width()
        h: typing.Optional[Decimal] = self._page.get_page_info().get_height()
        assert w is not None
        assert h is not None

        # add header
        if self._header_paint_method is not None:
            logger.debug(
                f"drawing header at {self._margin_left}, {h - self._margin_top}, {w - self._margin_right - self._margin_left} {self._margin_top}"
            )
            self._header_paint_method(
                self.get_page(),
                Rectangle(
                    self._margin_left,
                    h - self._margin_top,
                    w - self._margin_right - self._margin_left,
                    self._margin_top,
                ),
            )

        # add footer
        if self._footer_paint_method is not None:
            logger.debug(
                f"drawing footer at 0, 0, {w - self._margin_right - self._margin_left} {self._margin_bottom}"
            )
            self._footer_paint_method(
                self.get_page(),
                Rectangle(
                    self._margin_left,
                    Decimal(0),
                    w - self._margin_right - self._margin_left,
                    self._margin_bottom,
                ),
            )

        # return
        return self

    @staticmethod
    def _calculate_leading_between(e0: LayoutElement, e1: LayoutElement) -> Decimal:
        if e0 is None or e1 is None:
            return Decimal(0)
        from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText

        if isinstance(e0, ChunkOfText) or isinstance(e1, ChunkOfText):
            return max(
                (Decimal(1.2) * e0.get_font_size())
                if isinstance(e0, ChunkOfText)
                else Decimal(0),
                (Decimal(1.2) * e1.get_font_size())
                if isinstance(e1, ChunkOfText)
                else Decimal(0),
            )
        return Decimal(5)

    #
    # PUBLIC
    #

    def add(self, layout_element: LayoutElement) -> "PageLayout":
        """
        This method adds a `LayoutElement` to the current `Page`.
        The specific implementation of `PageLayout` should decide where the `LayoutElement` will be placed.
        :param layout_element:  the LayoutElement to be added
        :return:                self
        """

        # IF we are going out of bounds
        # THEN do nothing, return self
        if self._active_column >= self._number_of_columns:
            return self

        # IF the element being added is a Watermark
        # THEN just paint it (all over the Page)
        from borb.pdf.canvas.layout.image.watermark import Watermark

        if isinstance(layout_element, Watermark):
            # the actual Rectangle doesn't matter
            # it will be painted to fit the Page anyway
            layout_element.paint(
                self._page, Rectangle(Decimal(0), Decimal(0), Decimal(1), Decimal(1))
            )
            return self

        # get the dimensions of the Page
        page_width: typing.Optional[Decimal] = self._page.get_page_info().get_width()
        page_height: typing.Optional[Decimal] = self._page.get_page_info().get_height()
        assert page_width is not None
        assert page_height is not None

        # IF there is a previous LayoutElement,
        # THEN we use that to determine max y-coordinate
        max_y: Decimal = page_height - self._margin_top
        min_y: Decimal = self._margin_bottom
        if self._previous_layout_element is not None:
            previous_layout_box: typing.Optional[
                Rectangle
            ] = self._previous_layout_element.get_previous_layout_box()
            assert previous_layout_box is not None
            max_y = previous_layout_box.get_y()
            max_y -= MultiColumnLayout._calculate_leading_between(
                self._previous_layout_element, layout_element
            )
            max_y -= max(
                self._previous_layout_element.get_margin_bottom(),
                layout_element.get_margin_top(),
            )

        # calculate the height available for the LayoutElement
        available_height: Decimal = max_y - min_y

        # IF the available height is insufficient
        # THEN switch to a new column and try again
        if available_height < 0:
            self.switch_to_next_column()
            return self.add(layout_element)

        # calculate the available space (as a Rectangle) for the LayoutElement
        # fmt: off
        available_box: Rectangle = Rectangle(
            self._margin_left + sum(self._column_widths[0:self._active_column]) + sum(self._inter_column_margins[0:self._active_column]) + layout_element.get_margin_left(),
            min_y,
            self._column_widths[self._active_column] - layout_element.get_margin_right() - layout_element.get_margin_left(),
            available_height
        )
        # fmt: on

        # calculate the layout_box of the LayoutElement
        layout_box = layout_element.get_layout_box(available_box)

        # IF the layout_box is taller than the column
        # THEN raise an assert
        if round(layout_box.get_height(), 2) > round(available_box.get_height(), 2):
            if self._previous_layout_element is not None:
                self.switch_to_next_column()
                return self.add(layout_element)
            else:
                # fmt: off
                assert False, f"{layout_element.__class__.__name__} is too tall to fit inside column / page. Needed {round(layout_box.get_height())} pts, only {round(available_box.get_height())} pts available."
                # fmt: on

        # IF the layout_box is wider than the column
        # THEN raise an assert
        if round(layout_box.get_width(), 2) > round(
            self._column_widths[self._active_column], 2
        ):
            # fmt: off
            assert False, f"{layout_element.__class__.__name__} is too wide to fit inside column / page. Needed {round(layout_box.get_width())} pts, only {round(available_box.get_width())} pts available."
            # fmt: on

        # IF the content would be drawn in the margin_bottom
        # THEN switch to a new column
        if layout_box.y < self._margin_bottom:
            self.switch_to_next_column()
            return self.add(layout_element)

        # paint
        layout_element.paint(self._page, available_box)

        # store previous
        self._previous_layout_element = layout_element

        # return self
        return self

    def switch_to_next_column(self) -> "PageLayout":
        """
        This function forces this PageLayout to move to the next column on the Page
        :return:    self
        """
        self._active_column += 1
        if self._active_column == self._number_of_columns:
            return self.switch_to_next_page()
        self._previous_layout_element = None
        return self

    def switch_to_next_page(self) -> "PageLayout":
        """
        This function forces this PageLayout to move to the next Page
        :return:    self
        """
        self._active_column = 0
        self._previous_layout_element = None

        # get Document
        from borb.pdf.document.document import Document

        doc = self.get_page().get_root()
        assert isinstance(doc, Document)

        # determine page_width, page_height
        page_width: typing.Optional[Decimal] = self._page.get_page_info().get_width()
        page_height: typing.Optional[Decimal] = self._page.get_page_info().get_height()
        assert page_width is not None
        assert page_height is not None

        # create new Page
        from borb.pdf.page.page import Page

        self._page = Page(width=page_width, height=page_height)

        # add Page to Document
        doc.add_page(self._page)

        # return
        return self


class SingleColumnLayout(MultiColumnLayout):
    def __init__(self, page: "Page"):  # type: ignore[name-defined]
        w: typing.Optional[Decimal] = page.get_page_info().get_width()
        h: typing.Optional[Decimal] = page.get_page_info().get_height()
        assert w is not None
        assert h is not None
        super().__init__(
            page=page,
            column_widths=[w * Decimal(0.80)],
            footer_paint_method=None,
            header_paint_method=None,
            inter_column_margins=[],
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_top=h * Decimal(0.1),
        )


class ThreeColumnLayout(MultiColumnLayout):
    def __init__(self, page: "Page"):  # type: ignore[name-defined]
        w: typing.Optional[Decimal] = page.get_page_info().get_width()
        h: typing.Optional[Decimal] = page.get_page_info().get_height()
        assert w is not None
        assert h is not None
        super().__init__(
            page=page,
            column_widths=[
                w * Decimal(0.70) / Decimal(3),
                w * Decimal(0.70) / Decimal(3),
                w * Decimal(0.70) / Decimal(3),
            ],
            footer_paint_method=None,
            header_paint_method=None,
            inter_column_margins=[w * Decimal(0.05), w * Decimal(0.05)],
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_top=h * Decimal(0.1),
        )


class TwoColumnLayout(MultiColumnLayout):
    def __init__(self, page: "Page"):  # type: ignore[name-defined]
        w: typing.Optional[Decimal] = page.get_page_info().get_width()
        h: typing.Optional[Decimal] = page.get_page_info().get_height()
        assert w is not None
        assert h is not None
        super().__init__(
            page=page,
            column_widths=[
                w * Decimal(0.75) / Decimal(2),
                w * Decimal(0.75) / Decimal(2),
            ],
            footer_paint_method=None,
            header_paint_method=None,
            inter_column_margins=[w * Decimal(0.05)],
            margin_bottom=h * Decimal(0.1),
            margin_left=w * Decimal(0.1),
            margin_right=w * Decimal(0.1),
            margin_top=h * Decimal(0.1),
        )
