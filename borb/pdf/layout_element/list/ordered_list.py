#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an ordered list that extends the basic List functionality.

The `OrderedList` class automatically assigns an index number to each item in the list.
The index numbers follow a sequential pattern (e.g., 1, 2, 3) and are updated when new
items are appended. This class is useful for managing structured content such as
numbered lists in documents.
"""
import functools
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.list.list import List
from borb.pdf.layout_element.text.chunk import Chunk
from borb.pdf.layout_element.text.homogeneous_paragraph import HomogeneousParagraph
from borb.pdf.layout_element.text.paragraph import Paragraph
from borb.pdf.page import Page


class OrderedList(List):
    """
    Represents an ordered list that extends the basic List functionality.

    The `OrderedList` class automatically assigns an index number to each item in the list.
    The index numbers follow a sequential pattern (e.g., 1, 2, 3) and are updated when new
    items are appended. This class is useful for managing structured content such as
    numbered lists in documents.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new `OrderedList` object for rendering list elements in a PDF.

        This constructor allows customization of various layout and style properties
        for the list, such as margins, padding, borders, and alignment. These properties
        define the appearance and positioning of the list within the PDF page.

        :param background_color:        Optional background color for the list container.
        :param border_color:            Optional border color for the list container.
        :param border_dash_pattern:     Dash pattern used for the list border lines.
        :param border_dash_phase:       Phase offset for the dash pattern in the list borders.
        :param border_width_bottom:     Width of the bottom border of the list.
        :param border_width_left:       Width of the left border of the list.
        :param border_width_right:      Width of the right border of the list.
        :param border_width_top:        Width of the top border of the list.
        :param horizontal_alignment:    Horizontal alignment of the list (default is LEFT).
        :param margin_bottom:           Space between the list and the element below it.
        :param margin_left:             Space between the list and the left page margin.
        :param margin_right:            Space between the list and the right page margin.
        :param margin_top:              Space between the list and the element above it.
        :param padding_bottom:          Padding inside the list container at the bottom.
        :param padding_left:            Padding inside the list container on the left side.
        :param padding_right:           Padding inside the list container on the right side.
        :param padding_top:             Padding inside the list container at the top.
        :param vertical_alignment:      Vertical alignment of the list (default is TOP).
        """
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
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
        self.__index_items: typing.List[Chunk] = []

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def append_layout_element(self, layout_element: LayoutElement) -> "List":
        """
        Add a layout element to the list and update the index.

        This method adds a layout element (such as a text block, image, or another element)
        to the ordered list and updates the list's index by appending a new index item
        (e.g., a numbered label). The index for the newly added item is automatically
        incremented and formatted as a numbered chunk.

        :param layout_element:   The LayoutElement to be added.
        :return:    Self, to allow for method chaining.
        """
        super().append_layout_element(layout_element)

        # determine font_size to use (default 12)
        index_font_size: int = 12
        index_font_color: Color = X11Color.BLACK
        if isinstance(layout_element, Chunk):
            index_font_size = layout_element.get_font_size()
            index_font_color = layout_element.get_font_color()
        if isinstance(layout_element, HomogeneousParagraph) or isinstance(
            layout_element, Paragraph
        ):
            index_font_size = layout_element.get_font_size()
            index_font_color = layout_element.get_font_color()

        # add Chunk as index item
        n: int = len(self._List__list_items)  # type: ignore[attr-defined]
        self.__index_items.append(
            Chunk(text=f"{n}.", font_color=index_font_color, font_size=index_font_size)
        )  # type: ignore[attr-defined]

        # return
        return self

    @functools.cache
    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        # fmt: off
        avail_w: int = available_space[0] - self.get_padding_right() - self.get_padding_left()
        avail_h: int = available_space[1] - self.get_padding_top() - self.get_padding_bottom()
        # fmt: on

        # figure out the width of the widest index
        index_sizes: typing.List[typing.Tuple[int, int]] = [
            e.get_size(available_space=(avail_w, avail_h)) for e in self.__index_items
        ]
        w0: int = max([w for w, _ in index_sizes])

        # figure out the width of the widest item
        element_sizes: typing.List[typing.Tuple[int, int]] = [
            e.get_size(available_space=(avail_w - w0, avail_h))
            for e in self._List__list_items  # type: ignore[attr-defined]
        ]
        w1: int = max([w for w, _ in element_sizes])

        # calculate total_height
        total_height = sum(
            [max(s0[1], s1[1]) for s0, s1 in zip(index_sizes, element_sizes)]
        )

        # return
        return (
            w0 + 5 + w1 + self.get_padding_left() + self.get_padding_right(),
            total_height + self.get_padding_top() + self.get_padding_bottom(),
        )

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        # figure out the size
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))

        # figure out the width of the widest index
        w0: int = max(
            [
                i.get_size(available_space=(available_space[2], available_space[3]))[0]
                for i in self.__index_items
            ]
        )

        # figure out the width reserved for content items
        w1: int = w - 5 - self.get_padding_left() - self.get_padding_right() - w0

        # calculate where the background/borders need to be painted
        # fmt: off
        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.LEFT:
            background_x = available_space[0]
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)
        # fmt: on

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # BDC
        # fmt: off
        OrderedList._begin_marked_content_with_dictionary(page=page, structure_element_type='L')  # type: ignore[attr-defined]
        # fmt: on

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # loop over items, painting each in turn
        bottom_y: int = background_y + self.get_padding_bottom()
        for ch, el in [x for x in zip(self.__index_items, self._List__list_items)][::-1]:  # type: ignore[attr-defined]
            assert isinstance(ch, Chunk)
            assert isinstance(el, LayoutElement)

            # BDC
            # fmt: off
            OrderedList._begin_marked_content_with_dictionary(page=page, structure_element_type='LI')  # type: ignore[attr-defined]
            # fmt: on

            # paint index element
            elem_w, elem_h = el.get_size(available_space=(w1, h))
            index_w, index_h = ch.get_size(available_space=(w0, h))
            ch.paint(
                available_space=(
                    background_x + self.get_padding_left(),
                    bottom_y,
                    w0,
                    max(elem_h, index_h),
                ),
                page=page,
            )

            # paint item element
            el.paint(
                available_space=(
                    background_x + self.get_padding_left() + w0 + 5,
                    bottom_y,
                    w1,
                    max(elem_h, index_h),
                ),
                page=page,
            )

            # EMC
            OrderedList._end_marked_content(page=page)  # type: ignore[attr-defined]

            # next element(s) should be lower
            bottom_y += max(index_h, elem_h)

        # EMC
        OrderedList._end_marked_content(page=page)  # type: ignore[attr-defined]
