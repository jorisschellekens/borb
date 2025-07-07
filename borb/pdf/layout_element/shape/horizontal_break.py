#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a visual separation in a document, typically as a straight horizontal line.

The `HorizontalBreak` class is used to improve the structure and readability of a document
by clearly demarcating different sections of content. It can be inserted at any point in
the layout to serve as a divider, enhancing the visual organization of the content.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page


class HorizontalBreak(LayoutElement):
    """
    Represents a visual separation in a document, typically as a straight horizontal line.

    The `HorizontalBreak` class is used to improve the structure and readability of a document
    by clearly demarcating different sections of content. It can be inserted at any point in
    the layout to serve as a divider, enhancing the visual organization of the content.
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
        dash_pattern: typing.List[int] = [],
        dash_phase: int = 0,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        line_color: Color = X11Color.BLACK,
        line_width: int = 1,
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
        Initialize a new `HorizontalBreak` object for rendering a horizontal line break in a PDF.

        This constructor allows customization of various layout and style properties for
        the horizontal break, such as margins, padding, borders, dash patterns, and alignment.
        These properties define the appearance and positioning of the line within the PDF page.

        :param background_color:        Optional background color for the horizontal break container.
        :param border_color:            Optional border color for the horizontal break container.
        :param border_dash_pattern:     Dash pattern used for the container border lines.
        :param border_dash_phase:       Phase offset for the dash pattern in the container borders.
        :param border_width_bottom:     Width of the bottom border of the container.
        :param border_width_left:       Width of the left border of the container.
        :param border_width_right:      Width of the right border of the container.
        :param border_width_top:        Width of the top border of the container.
        :param dash_pattern:            Dash pattern used for the horizontal break line.
        :param dash_phase:              Phase offset for the dash pattern in the line.
        :param horizontal_alignment:    Horizontal alignment of the line (default is LEFT).
        :param line_color:              Color of the horizontal line (default is BLACK).
        :param line_width:              Width of the horizontal line.
        :param margin_bottom:           Space between the horizontal break and the element below it.
        :param margin_left:             Space between the horizontal break and the left page margin.
        :param margin_right:            Space between the horizontal break and the right page margin.
        :param margin_top:              Space between the horizontal break and the element above it.
        :param padding_bottom:          Padding inside the container at the bottom.
        :param padding_left:            Padding inside the container on the left side.
        :param padding_right:           Padding inside the container on the right side.
        :param padding_top:             Padding inside the container at the top.
        :param vertical_alignment:      Vertical alignment of the horizontal break (default is TOP).
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
        self.__dash_phase: int = dash_phase
        self.__dash_pattern: typing.List[int] = dash_pattern
        self.__line_color: Color = line_color
        self.__line_width: int = line_width

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_dash_pattern(self) -> typing.List[int]:
        """
        Retrieve the dash pattern used for stroking paths.

        The dash pattern controls the lengths of alternating dashes and gaps
        in a line. It is specified as a list of nonnegative integers, where
        each integer represents the length of a dash or a gap. The dash
        pattern must not consist solely of zeros.

        :return:    the line dash pattern
        """
        return [x for x in self.__dash_pattern]

    def get_dash_phase(self) -> int:
        """
        Get the dash phase for the line dash pattern.

        The dash phase specifies the distance into the dash pattern at which
        to start drawing. It is used in conjunction with a dash array to
        control the appearance of dashed lines. The dash phase is expressed
        in user space units.

        :return:    the line dash phase
        """
        return self.__dash_phase

    def get_line_color(self) -> Color:
        """
        Get the line color of this HorizontalBreak element.

        This method returns the color used for the line in a `HorizontalBreak`,
        which is typically a visual separator in the layout.

        :return: The `Color` object representing the line color of this `HorizontalBreak`.
        """
        return self.__line_color

    def get_line_width(self) -> int:
        """
        Retrieve the line width of this HorizontalBreak element.

        This method returns the width (thickness) of the line used in a `HorizontalBreak`,
        which is typically used as a visual divider in the document's layout.

        :return: The line width of this `HorizontalBreak`, represented as an integer.
        """
        return self.__line_width

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
            available_space[0],
            self.__line_width + self.get_padding_top() + self.get_padding_bottom(),
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
        # leading newline (if needed)
        HorizontalBreak._append_newline_to_content_stream(page)

        # store graphics state
        page["Contents"]["DecodedBytes"] += b"q\n"

        # set color
        rgb_line_color: RGBColor = self.__line_color.to_rgb_color()
        page["Contents"]["DecodedBytes"] += (
            f"{round(rgb_line_color.get_red() / 255, 7)} "
            f"{round(rgb_line_color.get_green() / 255, 7)} "
            f"{round(rgb_line_color.get_blue() / 255, 7)} rg\n"
        ).encode("latin1")

        # set width
        page["Contents"]["DecodedBytes"] += f"{self.__line_width} w\n".encode("latin1")

        # set dash pattern
        # fmt: off
        page["Contents"]["DecodedBytes"] += f"{self.__dash_pattern} {self.__dash_phase}d\n".encode('latin1')
        # fmt: on

        h: int = self.__line_width + self.get_padding_top() + self.get_padding_bottom()
        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # draw line
        # fmt: off
        page["Contents"]["DecodedBytes"] += f"{available_space[0] + self.get_padding_left()} {background_y} m\n".encode('latin1')
        page["Contents"]["DecodedBytes"] += f"{available_space[0] + available_space[2] - self.get_padding_right() - self.get_padding_left()} {background_y} l\n".encode('latin1')
        page["Contents"]["DecodedBytes"] += b"S\n"
        # fmt: on

        # set box
        self._LayoutElement__previous_paint_box = (
            0,
            background_y,
            available_space[2],
            h,
        )

        # restore graphics state
        page["Contents"]["DecodedBytes"] += b"Q\n"
