#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a progress bar element for visualizing task completion within a PDF document.

This class is designed to display a horizontal progress bar that reflects the completion
status of a task or process within a PDF layout. The progress bar can be customized for
appearance, size, and percentage completion.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.progress_bar.progress_bar import ProgressBar


class ProgressSquare(ProgressBar):
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
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        fill_color: Color = X11Color.GAINSBORO,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        max_value: int = 100,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        stroke_color: Color = X11Color.LIGHT_STEEL_BLUE,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
        width: int = 15,
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
            value=value,
            max_value=max_value,
            size=(width, width),
            stroke_color=stroke_color,
            fill_color=fill_color,
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

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
