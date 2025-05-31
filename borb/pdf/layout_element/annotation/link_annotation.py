#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a link annotation in a PDF document.

A link annotation can represent either a hypertext link to a destination elsewhere in the document
(see 12.3.2, “Destinations”) or an action to be performed (see 12.6, “Actions”).

Table 173 shows the annotation dictionary entries specific to this type of annotation.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.primitives import name


class LinkAnnotation(Annotation):
    """
    Represents a link annotation in a PDF document.

    A link annotation can represent either a hypertext link to a destination elsewhere in the document
    (see 12.3.2, “Destinations”) or an action to be performed (see 12.6, “Actions”).

    Table 173 shows the annotation dictionary entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        link_to_page_nr: int,
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
        size: typing.Tuple[int, int] = (100, 100),
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a remote GoTo annotation that links to a destination in another document or webpage.

        This constructor sets up a remote GoTo annotation, allowing users to create a clickable
        link that navigates to a specified destination in an external PDF document. You can customize
        the appearance of the annotation with various visual properties, including background and
        border colors, as well as dimensions.

        :param background_color:        Optional background color for the annotation.
        :param border_color:            Optional border color for the annotation.
        :param border_dash_pattern:     Dash pattern used for the annotation's border lines.
        :param border_dash_phase:       Phase offset for the dash pattern in the borders.
        :param border_width_bottom:     Width of the bottom border of the annotation.
        :param border_width_left:       Width of the left border of the annotation.
        :param border_width_right:      Width of the right border of the annotation.
        :param border_width_top:        Width of the top border of the annotation.
        :param horizontal_alignment:     Horizontal alignment of the annotation (default is LEFT).
        :param margin_bottom:           Space between the annotation and the element below it.
        :param margin_left:             Space between the annotation and the left page margin.
        :param margin_right:            Space between the annotation and the right page margin.
        :param margin_top:              Space between the annotation and the element above it.
        :param padding_bottom:          Padding inside the annotation at the bottom.
        :param padding_left:            Padding inside the annotation on the left side.
        :param padding_right:           Padding inside the annotation on the right side.
        :param padding_top:             Padding inside the annotation at the top.
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
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            size=size,
            vertical_alignment=vertical_alignment,
        )
        # (Required) The type of annotation that this dictionary describes; shall be
        # Link for a link annotation.
        self[name("Subtype")] = name("Link")

        # (Optional; not permitted if an A entry is present) A destination that shall
        # be displayed when the annotation is activated (see 12.3.2,
        # “Destinations”
        self[name("Dest")] = [link_to_page_nr, name("Fit")]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
