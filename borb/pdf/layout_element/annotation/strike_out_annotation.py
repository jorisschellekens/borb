#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a strikeout text markup annotation.

Strikeout annotations (PDF 1.3) appear as strikethroughs in the text of a document.
They may also include highlights, underlines, and jagged ("squiggly") underlines, which
are supported in PDF 1.4. When opened, they display a pop-up window containing the text
of the associated note. Table 179 shows the annotation dictionary entries specific to
these types of annotations.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.primitives import name, stream


class StrikeOutAnnotation(Annotation):
    """
    Represents a strikeout text markup annotation.

    Strikeout annotations (PDF 1.3) appear as strikethroughs in the text of a document.
    They may also include highlights, underlines, and jagged ("squiggly") underlines, which
    are supported in PDF 1.4. When opened, they display a pop-up window containing the text
    of the associated note. Table 179 shows the annotation dictionary entries specific to
    these types of annotations.
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
        line_width: int = 1,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: typing.Tuple[int, int] = (100, 100),
        stroke_color: Color = X11Color.YELLOW_MUNSELL,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a StrikeOutAnnotation object for creating a strikethrough effect on content in a PDF document.

        This annotation allows users to highlight sections of text or content with a strikethrough line. It offers
        customization options for the background, border, line color, and size. Additional properties like margins,
        padding, and alignment are also adjustable to integrate smoothly with various document layouts.

        :param background_color:        The background color of the annotation. Defaults to None (transparent).
        :param border_color:            The color of the annotation's border. Defaults to None.
        :param border_dash_pattern:     A list specifying the dash pattern for the annotation's border. Defaults to an empty list (solid border).
        :param border_dash_phase:       The phase offset for the border dash pattern. Defaults to 0.
        :param border_width_bottom:     The width of the bottom border of the annotation. Defaults to 0.
        :param border_width_left:       The width of the left border of the annotation. Defaults to 0.
        :param border_width_right:      The width of the right border of the annotation. Defaults to 0.
        :param border_width_top:        The width of the top border of the annotation. Defaults to 0.
        :param contents:                Optional text content to display as part of the annotation. Defaults to None.
        :param horizontal_alignment:    The horizontal alignment of the annotation (e.g., left, center, right). Defaults to LEFT.
        :param line_width:              The width of the strikethrough line. Defaults to 1.
        :param margin_bottom:           The bottom margin of the annotation. Defaults to 0.
        :param margin_left:             The left margin of the annotation. Defaults to 0.
        :param margin_right:            The right margin of the annotation. Defaults to 0.
        :param margin_top:              The top margin of the annotation. Defaults to 0.
        :param padding_bottom:          The bottom padding inside the annotation, between the content and the border. Defaults to 0.
        :param padding_left:            The left padding inside the annotation. Defaults to 0.
        :param padding_right:           The right padding inside the annotation. Defaults to 0.
        :param padding_top:             The top padding inside the annotation. Defaults to 0.
        :param size:                    A tuple specifying the width and height of the annotation. Defaults to (100, 100).
        :param stroke_color:            The color of the strikethrough line (default is yellow). Defaults to X11Color.YELLOW_MUNSELL.
        :param vertical_alignment:      The vertical alignment of the annotation (e.g., top, middle, bottom). Defaults to TOP.
        """
        assert line_width >= 0, "The line_width must be a non-negative value."
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
            padding_top=padding_top,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            size=size,
            stroke_color=stroke_color,
            vertical_alignment=vertical_alignment,
        )

        # (Required) The type of annotation that this dictionary describes; shall
        # be Highlight, Underline, Squiggly, or StrikeOut for a highlight,
        # underline, squiggly-underline, or strikeout annotation, respectively.
        self["Subtype"] = name("StrikeOut")

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

        # (Optional; PDF 1.2) An appearance dictionary specifying how the
        # annotation shall be presented visually on the page (see 12.5.5,
        # “Appearance Streams”). Individual annotation handlers may ignore this
        # entry and provide their own appearances.
        self[name("AP")] = {
            name("N"): stream(
                {name("Type"): name("XObject"), name("Subtype"): name("Form")}
            )
        }

        # set /AP/N (to draw the strikethrough)
        rgb_stroke_color: RGBColor = stroke_color.to_rgb_color()
        ap_n_content: str = (
            f"q "
            f"{rgb_stroke_color.get_red()/255} {rgb_stroke_color.get_green()/255} {rgb_stroke_color.get_blue()/255} RG "
            f"{line_width} w "
            f"0 5 m {size[0]} 5 l S Q"
        )
        import zlib

        self[name("AP")][name("N")][name("Bytes")] = zlib.compress(
            ap_n_content.encode("latin1")
        )
        self[name("AP")][name("N")][name("Length")] = len(ap_n_content.encode("latin1"))
        self["AP"]["N"][name("Filter")] = name("FlateDecode")
        self["AP"]["N"][name("BBox")] = [0, 0, size[0], size[1]]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
