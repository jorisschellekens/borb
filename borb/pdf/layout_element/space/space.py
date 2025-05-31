#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class representing an empty space in a PDF layout.

This element does not render any content but occupies a defined space.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page


class Space(LayoutElement):
    """
    A class representing an empty space in a PDF layout.

    This element does not render any content but occupies a defined space.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        size: typing.Tuple[int, int],
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
        Initialize a Space element with a specified size and alignment.

        This element only uses `size`, `horizontal_alignment`, and `vertical_alignment`.
        Other parameters (e.g., background, borders, margins, padding) are ignored.

        :param size: A tuple (width, height) representing the size of the space. Width and height must be non-negative.
        :param horizontal_alignment: Horizontal alignment of the space (default: LEFT).
        :param vertical_alignment: Vertical alignment of the space (default: TOP).
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
        assert size[0] >= 0, "Width must be non-negative"
        assert size[1] >= 0, "Height must be non-negative"
        self.__size: typing.Tuple[int, int] = size

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
        return self.__size

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
        w: int = self.__size[0]
        h: int = self.__size[1]

        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)
