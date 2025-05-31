#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a circle annotation in a PDF document.

Circle annotations (PDF 1.3) display an ellipse on the page. When opened, they show a pop-up
window containing the text of the associated note. The ellipse is inscribed within the annotation
rectangle defined by the annotation dictionary's Rect entry (see Table 168).
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.primitives import name


class CircleAnnotation(Annotation):
    """
    Represents a circle annotation in a PDF document.

    Circle annotations (PDF 1.3) display an ellipse on the page. When opened, they show a pop-up
    window containing the text of the associated note. The ellipse is inscribed within the annotation
    rectangle defined by the annotation dictionary's Rect entry (see Table 168).
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
        fill_color: typing.Optional[Color] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: typing.Tuple[int, int] = (100, 100),
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new `CircleAnnotation` object for rendering a circular annotation in a PDF.

        This constructor allows customization of various layout and style properties for
        the circle annotation, such as background color, border, fill color, size,
        contents, and alignment. These properties define the appearance and positioning of
        the circular annotation within the PDF page.

        :param background_color:         Optional background color for the circle annotation.
        :param border_color:             Optional border color for the annotation container.
        :param border_dash_pattern:      Dash pattern used for the annotation border lines.
        :param border_dash_phase:        Phase offset for the dash pattern in the annotation borders.
        :param border_width_bottom:      Width of the bottom border of the annotation container.
        :param border_width_left:        Width of the left border of the annotation container.
        :param border_width_right:       Width of the right border of the annotation container.
        :param border_width_top:         Width of the top border of the annotation container.
        :param contents:                 Optional text content for the annotation.
        :param fill_color:               Optional fill color for the circle annotation.
        :param horizontal_alignment:     Horizontal alignment of the annotation (default is LEFT).
        :param padding_bottom:           Padding inside the annotation container at the bottom.
        :param padding_left:             Padding inside the annotation container on the left side.
        :param padding_right:            Padding inside the annotation container on the right side.
        :param padding_top:              Padding inside the annotation container at the top.
        :param size:                     Tuple representing the width and height of the annotation.
        :param stroke_color:             Color of the circle's stroke (default is BLACK).
        :param vertical_alignment:       Vertical alignment of the annotation (default is TOP).
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
            fill_color=fill_color,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            size=size,
            stroke_color=stroke_color,
            vertical_alignment=vertical_alignment,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Square or Circle for a square or circle annotation, respectively.
        self["Subtype"] = name("Circle")

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
