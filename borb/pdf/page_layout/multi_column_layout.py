#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a layout for organizing content into multiple columns on a PDF page.

The `MultiColumnLayout` class provides a flexible way to arrange content in
multiple columns, such as two, three, or more, depending on the needs of the
document. It is designed to manage the flow of text and other elements across
these columns, ensuring proper alignment and balance. Content automatically
flows from one column to the next and, if necessary, across pages.

This layout is ideal for presenting structured information in a visually
appealing manner, improving readability and allowing for an even distribution
of content on the page.
"""
import typing

from borb.pdf.document import Document
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.list import List
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.layout_element.table.table import Table
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page
from borb.pdf.page_layout.page_layout import PageLayout


class MultiColumnLayout(PageLayout):
    """
    Represents a layout for organizing content into multiple columns on a PDF page.

    The `MultiColumnLayout` class provides a flexible way to arrange content in
    multiple columns, such as two, three, or more, depending on the needs of the
    document. It is designed to manage the flow of text and other elements across
    these columns, ensuring proper alignment and balance. Content automatically
    flows from one column to the next and, if necessary, across pages.

    This layout is ideal for presenting structured information in a visually
    appealing manner, improving readability and allowing for an even distribution
    of content on the page.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        page: Page,
        inter_column_margin: typing.Optional[int] = None,
        margin_bottom: typing.Optional[int] = None,
        margin_left: typing.Optional[int] = None,
        margin_right: typing.Optional[int] = None,
        margin_top: typing.Optional[int] = None,
        number_of_columns: int = 2,
    ):
        """
        Initialize the MultiColumnLayout with the specified page and number of columns.

        The `MultiColumnLayout` constructor sets up a layout that organizes content
        into multiple columns on the provided PDF page.
        This layout is designed to facilitate the presentation of information
        in a structured and visually appealing manner.
        It automatically calculates the dimensions and margins for the specified number of columns,
        ensuring that content flows smoothly across the columns while maintaining appropriate spacing.

        :param page:                An instance of the `Page` class that represents the page where the multi-column layout will be applied.
                                    This instance provides the dimensions necessary for layout configuration.
        :param number_of_columns:   An integer that specifies the number of columns for the layout.
                                    The default value is 2, but it can be adjusted to accommodate different content requirements.
        """
        self.__page: Page = page
        self.__page_width, self._page_height = page.get_size()
        self.__page_margin_left: int = margin_left or int(self.__page_width * 0.1)
        self.__page_margin_right: int = margin_right or int(self.__page_width * 0.1)
        self.__page_margin_top: int = margin_top or int(self._page_height * 0.1)
        self.__page_margin_bottom: int = margin_bottom or int(self._page_height * 0.1)
        self.__inter_column_margin: int = inter_column_margin or 14

        # calculate w_avail
        # fmt: off
        w_avail: int = self.__page_width - self.__page_margin_left - self.__page_margin_right
        w_avail -= (number_of_columns - 1) * self.__inter_column_margin
        # fmt: on

        # calculate __column_widths
        # fmt: off
        self.__column_widths: typing.List[int] = [w_avail // number_of_columns for _ in range(0, number_of_columns)]
        self.__column_widths[0] += w_avail - sum(self.__column_widths)
        # fmt: on

        self.__previous_element_bottom: int = self._page_height - self.__page_margin_top
        self.__previous_element_margin_bottom: int = 0
        self.__previous_element_column: int = 0
        self.__is_first_element_in_column: bool = True

    #
    # PRIVATE
    #

    @staticmethod
    def __get_calculated_margin_bottom(e: LayoutElement) -> int:
        if e.get_margin_bottom() != 0:
            return e.get_margin_bottom()
        if isinstance(e, Chunk):
            return int(e.get_font_size() * 1.2)
        if isinstance(e, Paragraph):
            return int(e.get_font_size() * 1.2)
        if isinstance(e, Image) or isinstance(e, Shape):
            return 14
        if isinstance(e, List) or isinstance(e, Table):
            return 14
        return 14

    @staticmethod
    def __get_leading_or_margin_top(e: LayoutElement) -> int:
        if e.get_margin_top() != 0:
            return e.get_margin_top()
        if isinstance(e, Chunk):
            return int(e.get_font_size() * 1.2)
        if isinstance(e, Paragraph):
            return int(e.get_font_size() * 1.2)
        if isinstance(e, Image) or isinstance(e, Shape):
            return 14
        if isinstance(e, List) or isinstance(e, Table):
            return 14
        return 14

    #
    # PUBLIC
    #

    def append_layout_element(
        self, layout_element: LayoutElement
    ) -> "MultiColumnLayout":
        """
        Append a layout element to the multi-column layout.

        This method adds the specified layout element, such as text, images, or other
        visual components, to the current multi-column layout. The element is
        positioned within the available columns and will flow from one column to
        the next if needed, maintaining the structured layout of the content.

        :param layout_element:   the LayoutElement to be added
        :return:    Self, this allows for method-chaining
        """
        # IF no margin_top is specified
        # THEN calculate one
        margin_top: int = MultiColumnLayout.__get_leading_or_margin_top(layout_element)

        # IF this is the first LayoutElement being added to the very first Page (managed by this SingleColumnLayout)
        # THEN we don't care about margin_top (equivalent to this SingleColumnLayout starting a new Page)
        if self.__is_first_element_in_column:
            margin_top = 0
            self.__is_first_element_in_column = False
            self.__previous_element_bottom = self._page_height - self.__page_margin_top
            self.__previous_element_margin_bottom = 0

        # determine the available space
        # fmt: off
        w_avail: int = self.__column_widths[self.__previous_element_column]
        h_avail: int = self.__previous_element_bottom - self.__page_margin_bottom - max(self.__previous_element_margin_bottom, margin_top)
        h_avail_full: int = (self._page_height - self.__page_margin_top - self.__page_margin_bottom)
        # fmt: on

        # determine the space of the LayoutElement
        w, h = layout_element.get_size(available_space=(w_avail, h_avail))

        # check width
        assert (
            w <= w_avail
        ), f"{layout_element} is too wide, needed {w} pts, {w_avail} pts available"

        # check height
        # fmt: off
        assert h <= h_avail_full, f"{layout_element} is too tall, needed {h} pts, {h_avail_full} pts available"
        # fmt: on

        # IF we can fill the current column
        # THEN do that
        if w <= w_avail and h <= h_avail:

            # place LayoutElement on the Page
            # fmt: off
            layout_element.paint(
                available_space=(
                    self.__page_margin_left + sum([cw for cw in self.__column_widths[: self.__previous_element_column]]+ [0]) + (self.__previous_element_column * self.__inter_column_margin),
                    self.__page_margin_bottom,
                    w_avail,
                    h_avail,
                ),
                page=self.__page,
            )
            # fmt: on

            # move _previous_element_bottom
            # fmt: off
            previous_paint_box: typing.Optional[typing.Tuple[int, int, int, int]] = layout_element.get_previous_paint_box()
            assert previous_paint_box is not None
            self.__previous_element_bottom = previous_paint_box[1]
            # fmt: on

            # IF no margin_bottom is specified
            # THEN calculate one
            self.__previous_element_margin_bottom = (
                MultiColumnLayout.__get_calculated_margin_bottom(layout_element)
            )

            # return
            return self

        # IF we can't fit this in the current column
        # THEN try the next one
        if h > h_avail:
            self.next_column()
            return self.append_layout_element(layout_element)

        # IF we got there
        # THEN something went wrong
        assert False

    def next_column(self) -> "MultiColumnLayout":
        """
        Move to the next column in the layout, adding a new page if necessary.

        This method manages the transition to the next column in a multi-column layout.
        If there are no more columns on the current page, a new page is added,
        and the column index is reset to the first column. The layout manager
        updates its internal state to reflect the transition.

        :return: The updated MultiColumnLayout instance.
        """
        self.__previous_element_column += 1
        # IF we ran out of columns
        # THEN add the next Page, and reset
        if self.__previous_element_column == len(self.__column_widths):
            self.next_page()
            return self
        self.__is_first_element_in_column = True
        self.__previous_element_bottom = self._page_height - self.__page_margin_top
        self.__previous_element_margin_bottom = 0
        return self

    def next_page(self) -> "MultiColumnLayout":
        """
        Add a new page to the layout and reset column tracking.

        This method handles transitioning to a new page in the multi-column layout.
        It appends a new page to the associated document, resets the column index,
        and updates the internal layout state to reflect the change.

        :return: The updated MultiColumnLayout instance.
        """
        doc: typing.Optional[Document] = self.__page.get_document()
        assert doc is not None
        self.__page = Page(
            height_in_points=self.__page.get_size()[1],
            width_in_points=self.__page.get_size()[0],
        )
        doc.append_page(self.__page)
        self.__is_first_element_in_column = True
        self.__previous_element_bottom = self._page_height - self.__page_margin_top
        self.__previous_element_column = 0
        self.__previous_element_margin_bottom = 0
        return self
