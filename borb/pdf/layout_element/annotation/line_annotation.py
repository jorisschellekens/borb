#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a line annotation in a PDF document.

A line annotation (PDF 1.3) displays a single straight line on the page. When opened,
it displays a pop-up window containing the text of the associated note.

Table 175 shows the annotation dictionary entries specific to this type of annotation.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement


class LineAnnotation(Annotation):
    """
    Represents a line annotation in a PDF document.

    A line annotation (PDF 1.3) displays a single straight line on the page. When opened,
    it displays a pop-up window containing the text of the associated note.

    Table 175 shows the annotation dictionary entries specific to this type of annotation.
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
        contents: typing.Optional[str] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: int = 100,
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a LineAnnotation for customizable line-based PDF annotations.

        :param background_color: Background color of the line annotation area.
        :param border_color: Border color for the line annotation.
        :param border_dash_pattern: Dash pattern for the annotation border.
        :param border_dash_phase: Starting phase for the dashed border.
        :param border_width_bottom: Width of the bottom border.
        :param border_width_left: Width of the left border.
        :param border_width_right: Width of the right border.
        :param border_width_top: Width of the top border.
        :param contents: Optional text content for the annotation.
        :param horizontal_alignment: Horizontal alignment within the layout.
        :param margin_bottom: Bottom margin for spacing.
        :param margin_left: Left margin for spacing.
        :param margin_right: Right margin for spacing.
        :param margin_top: Top margin for spacing.
        :param padding_bottom: Bottom padding inside the annotation.
        :param padding_left: Left padding inside the annotation.
        :param padding_right: Right padding inside the annotation.
        :param padding_top: Top padding inside the annotation.
        :param size: Size of the annotation.
        :param stroke_color: Stroke color for the annotation line.
        :param vertical_alignment: Vertical alignment within the layout.
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
            contents=contents,
            fill_color=None,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            size=(size, 1),
            stroke_color=stroke_color,
            vertical_alignment=vertical_alignment,
        )
        # TODO

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
