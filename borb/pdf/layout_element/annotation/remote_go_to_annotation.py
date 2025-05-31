#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a remote go-to annotation, which is a type of link annotation.

A remote go-to annotation allows for a hypertext link to a destination outside the document
(see 12.3.2, “Destinations”) or an action to be performed (see 12.6, “Actions”).
Table 173 shows the annotation dictionary entries specific to this type of annotation.

This annotation facilitates linking to a remote Uniform Resource Identifier (URI), enabling
users to navigate to external content or resources when activated.
"""

import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import name


class RemoteGoToAnnotation(Annotation):
    """
    Represents a remote go-to annotation, which is a type of link annotation.

    A remote go-to annotation allows for a hypertext link to a destination outside the document
    (see 12.3.2, “Destinations”) or an action to be performed (see 12.6, “Actions”).
    Table 173 shows the annotation dictionary entries specific to this type of annotation.

    This annotation facilitates linking to a remote Uniform Resource Identifier (URI), enabling
    users to navigate to external content or resources when activated.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        uri: str,
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

        # (Optional) An array specifying the characteristics of the annotation’s
        # border, which shall be drawn as a rounded rectangle.
        # (PDF 1.0) The array consists of three numbers defining the horizontal
        # corner radius, vertical corner radius, and border width, all in default user
        # space units. If the corner radii are 0, the border has square (not rounded)
        # corners; if the border width is 0, no border is drawn.
        # (PDF 1.1) The array may have a fourth element, an optional dash array
        # defining a pattern of dashes and gaps that shall be used in drawing the
        # border. The dash array shall be specified in the same format as in the
        # line dash pattern parameter of the graphics state (see 8.4.3.6, “Line
        # Dash Pattern”).
        # EXAMPLE
        # A Border value of [ 0 0 1 [ 3 2 ] ] specifies a border 1
        # unit wide, with square corners, drawn with 3-unit
        # dashes alternating with 2-unit gaps.
        # NOTE
        # (PDF 1.2) The dictionaries for some annotation types (such
        # as free text and polygon annotations) can include the BS
        # entry. That entry specifies a border style dictionary that has
        # more settings than the array specified for the Border entry.
        # If an annotation dictionary includes the BS entry, then the
        # Border entry is ignored.
        # Default value: [ 0 0 1 ].
        self[name("Border")] = [0, 0, 0]

        # (Optional; PDF 1.1) An action that shall be performed when the link
        # annotation is activated (see 12.6, “Actions”).
        self[name("A")] = {
            name("S"): name("URI"),
            name("Type"): name("Action"),
            name("URI"): uri,
        }

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

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
        # call super
        super().paint(available_space=available_space, page=page)
