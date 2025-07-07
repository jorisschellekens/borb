#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a progress bar element for visualizing task completion within a PDF document.

This class is designed to display a horizontal progress bar that reflects the completion
status of a task or process within a PDF layout. The progress bar can be customized for
appearance, size, and percentage completion.
"""
import functools
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page


class ProgressBar(LayoutElement):
    """
    Represents a progress bar element for visualizing task completion within a PDF document.

    This class is designed to display a horizontal progress bar that reflects the completion
    status of a task or process within a PDF layout. The progress bar can be customized for
    appearance, size, and percentage completion.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        value: int,
        max_value: int = 100,
        size: typing.Tuple[int, int] = (121, 15),
        stroke_color: Color = X11Color.LIGHT_STEEL_BLUE,
        fill_color: Color = X11Color.GAINSBORO,
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
        Initialize a ProgressBar object with customizable attributes.

        The `ProgressBar` class represents a visual progress bar, which can be customized in terms of value,
        size, color, alignment, and margins.
        It supports defining the progress level (`value`),
        appearance (such as fill color, stroke color, and border settings),
        and positioning (via padding, margin, and alignment).

        :param value:               The current progress value (e.g., 40 out of 100).
        :param max_value:           The maximum value of the progress bar, default is 100.
        :param size:                A tuple representing the width and height of the progress bar, default is (121, 15).
        :param stroke_color:        The color of the bar's stroke or outline, default is `X11Color.LIGHT_STEEL_BLUE`.
        :param fill_color:          The color used to fill the progress bar, default is `X11Color.GAINSBORO`.
        :param background_color:    Optional background color for the progress bar, defaults to None.
        :param border_color:        Optional border color for the progress bar, defaults to None.
        :param border_dash_pattern: A list specifying dash patterns for the border, default is an empty list (no dashes).
        :param border_dash_phase:   An integer representing the phase of the border dash pattern, default is 0.
        :param border_width_bottom: The bottom border width, default is 0.
        :param border_width_left:   The left border width, default is 0.
        :param border_width_right:  The right border width, default is 0.
        :param border_width_top:    The top border width, default is 0.
        :param horizontal_alignment: Horizontal alignment of the progress bar, default is `LayoutElement.HorizontalAlignment.LEFT`.
        :param margin_bottom:       The bottom margin in points, default is 0.
        :param margin_left:         The left margin in points, default is 0.
        :param margin_right:        The right margin in points, default is 0.
        :param margin_top:          The top margin in points, default is 0.
        :param padding_bottom:      The bottom padding in points, default is 0.
        :param padding_left:        The left padding in points, default is 0.
        :param padding_right:       The right padding in points, default is 0.
        :param padding_top:         The top padding in points, default is 0.
        :param vertical_alignment:  Vertical alignment of the progress bar, default is `LayoutElement.VerticalAlignment.TOP`.
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
        assert value >= 0, "The value must be a non-negative value."
        assert max_value > 0, "The max_value must be a non-negative value."
        assert max_value >= value
        assert size[0] > 0
        assert size[1] > 0
        self.__value: int = value
        self.__max_value: int = max_value
        self.__size: typing.Tuple[int, int] = size
        self.__stroke_color: Color = stroke_color
        self.__fill_color: Color = fill_color

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

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
        return (
            self.__size[0] + self.get_padding_left() + self.get_padding_right(),
            self.__size[1] + self.get_padding_top() + self.get_padding_bottom(),
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

        # leading newline (if needed)
        ProgressBar._append_newline_to_content_stream(page)

        # store graphics state
        page["Contents"]["DecodedBytes"] += b"q\n"

        # rectangle (representing the available bar)
        rgb_fill_color: RGBColor = self.__fill_color.to_rgb_color()
        page["Contents"]["DecodedBytes"] += (
            f"{rgb_fill_color.get_red() / 255} "
            f"{rgb_fill_color.get_green() / 255} "
            f"{rgb_fill_color.get_blue() / 255} rg\n"
        ).encode("latin1")
        page["Contents"]["DecodedBytes"] += (
            f"{rgb_fill_color.get_red() / 255} "
            f"{rgb_fill_color.get_green() / 255} "
            f"{rgb_fill_color.get_blue() / 255} RG\n"
        ).encode("latin1")
        page["Contents"]["DecodedBytes"] += (
            f"{background_x + self.get_padding_left()} "
            f"{background_y + self.get_padding_top()} "
            f"{self.__size[0]} "
            f"{self.__size[1]} re\n"
        ).encode("latin1")
        page["Contents"]["DecodedBytes"] += b"B\n"

        # rectangle (representing the progress)
        rgb_stroke_color: RGBColor = self.__stroke_color.to_rgb_color()
        page["Contents"]["DecodedBytes"] += (
            f"{rgb_stroke_color.get_red() / 255} "
            f"{rgb_stroke_color.get_green() / 255} "
            f"{rgb_stroke_color.get_blue() / 255} rg\n"
        ).encode("latin1")
        page["Contents"]["DecodedBytes"] += (
            f"{rgb_stroke_color.get_red() / 255} "
            f"{rgb_stroke_color.get_green() / 255} "
            f"{rgb_stroke_color.get_blue() / 255} RG\n"
        ).encode("latin1")
        page["Contents"]["DecodedBytes"] += (
            f"{background_x + self.get_padding_left()} "
            f"{background_y + self.get_padding_top()} "
            f"{self.__size[0] * (self.__value / self.__max_value)} "
            f"{self.__size[1]} re\n"
        ).encode("latin1")
        page["Contents"]["DecodedBytes"] += b"B\n"

        # restore graphics state
        page["Contents"]["DecodedBytes"] += b"Q\n"
