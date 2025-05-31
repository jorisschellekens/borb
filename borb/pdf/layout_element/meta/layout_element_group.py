#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A group of layout elements arranged with specified positions and sizes.

This class represents a collection of `LayoutElement` objects, each placed at a
specific position and with a defined size. It extends `LayoutElement` and supports
rendering onto a `Page` while respecting layout properties such as alignment,
margins, padding, and borders.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page


class LayoutElementGroup(LayoutElement):
    """
    A group of layout elements arranged with specified positions and sizes.

    This class represents a collection of `LayoutElement` objects, each placed at a
    specific position and with a defined size. It extends `LayoutElement` and supports
    rendering onto a `Page` while respecting layout properties such as alignment,
    margins, padding, and borders.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        layout_elements: typing.List[LayoutElement],
        positions: typing.List[typing.Tuple[int, int]],
        sizes: typing.List[typing.Tuple[int, int]],
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
        Initialize a new LayoutElementGroup object for rendering a group of LayoutElements in a PDF.

        This constructor allows customization of various layout and style properties
        for the group, such as margins, padding, borders, and alignment. These properties
        define the appearance and positioning of the group within the PDF page.

        :param layout_elements:         The LayoutElement objects in this group
        :param positions:               The (relative) positions of the LayoutElements in this group
        :param sizes:                   The (absolute) sizes of the LayoutElements in this group
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
        assert len(layout_elements) == len(positions)
        assert len(layout_elements) == len(sizes)
        self.__layout_elements: typing.List[LayoutElement] = layout_elements
        self.__positions: typing.List[typing.Tuple[int, int]] = positions
        self.__sizes: typing.List[typing.Tuple[int, int]] = sizes

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

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
        K: int = len(self.__layout_elements)
        min_x: typing.Optional[int] = None
        min_y: typing.Optional[int] = None
        max_x: typing.Optional[int] = None
        max_y: typing.Optional[int] = None
        for i in range(0, K):
            if min_x is None or min_x > self.__positions[i][0]:
                min_x = self.__positions[i][0]
            if min_y is None or min_y > self.__positions[i][1]:
                min_y = self.__positions[i][1]
            if max_x is None or max_x < self.__positions[i][0] + self.__sizes[i][0]:
                max_x = self.__positions[i][0] + self.__sizes[i][0]
            if max_y is None or max_y < self.__positions[i][1] + self.__sizes[i][1]:
                max_y = self.__positions[i][1] + self.__sizes[i][1]
        assert min_x is not None
        assert min_y is not None
        assert max_x is not None
        assert max_y is not None
        return max_x - min_x, max_y - min_y

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
        # calculate width and height
        w, h = self.get_size(available_space=(available_space[2], available_space[3]))

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

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # calculate delta_x / delta_y
        K: int = len(self.__layout_elements)
        delta_x: typing.Optional[int] = None
        delta_y: typing.Optional[int] = None
        for i in range(0, K):
            if delta_x is None or delta_x > self.__positions[i][0]:
                delta_x = self.__positions[i][0]
            if delta_y is None or delta_y > self.__positions[i][1]:
                delta_y = self.__positions[i][1]
        assert delta_x is not None
        assert delta_y is not None

        # paint
        for i in range(0, K):
            self.__layout_elements[i].paint(
                available_space=(
                    self.__positions[i][0] - delta_x + background_x,
                    self.__positions[i][1] - delta_y + background_y,
                    self.__sizes[i][0],
                    self.__sizes[i][1],
                ),
                page=page,
            )
