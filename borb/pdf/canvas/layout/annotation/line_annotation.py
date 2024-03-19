#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The purpose of a line annotation (PDF 1.3) is to display a single straight line on the page. When opened, it shall
display a pop-up window containing the text of the associated note. Table 175 shows the annotation dictionary
entries specific to this type of annotation.
"""
import typing
from decimal import Decimal

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation
from borb.pdf.canvas.layout.annotation.polyline_annotation import LineEndStyleType


class LineAnnotation(Annotation):
    """
    The purpose of a line annotation (PDF 1.3) is to display a single straight line on the page. When opened, it shall
    display a pop-up window containing the text of the associated note. Table 175 shows the annotation dictionary
    entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        start_point: typing.Tuple[Decimal, Decimal],
        end_point: typing.Tuple[Decimal, Decimal],
        left_line_end_style: LineEndStyleType = LineEndStyleType.NONE,
        right_line_end_style: LineEndStyleType = LineEndStyleType.NONE,
        stroke_color: Color = HexColor("000000"),
    ):
        x = min([start_point[0], end_point[0]])
        y = min([start_point[1], end_point[1]])
        w = max([start_point[0], end_point[0]]) - x
        h = max([start_point[1], end_point[1]]) - y

        # create generic annotation
        super(LineAnnotation, self).__init__(
            bounding_box=Rectangle(x, y, w, h), color=stroke_color
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Line for a line annotation.
        self[Name("Subtype")] = Name("Line")

        # (Required) An array of four numbers, [ x 1 y 1 x 2 y 2 ], specifying the
        # starting and ending coordinates of the line in default user space.
        # If the LL entry is present, this value shall represent the endpoints of the
        # leader lines rather than the endpoints of the line itself; see Figure 60.
        self[Name("L")] = List().set_is_inline(True)
        self["L"].append(start_point[0])
        self["L"].append(start_point[1])
        self["L"].append(end_point[0])
        self["L"].append(end_point[1])

        # (Optional; PDF 1.4) An array of two names specifying the line ending
        # styles that shall be used in drawing the line. The first and second
        # elements of the array shall specify the line ending styles for the endpoints
        # defined, respectively, by the first and second pairs of coordinates, (x 1 , y 1 )
        # and (x 2 , y 2 ), in the L array. Table 176 shows the possible values. Default
        # value: [ /None /None ].
        self[Name("LE")] = List().set_is_inline(True)
        self["LE"].append(left_line_end_style.value)
        self["LE"].append(right_line_end_style)

        # (Optional; PDF 1.4) An array of numbers that shall be in the range 0.0 to
        # 1.0 and shall specify the interior color with which to fill the annotation’s
        # rectangle or ellipse. The number of array elements determines the colour
        # space in which the colour shall be defined
        if stroke_color is not None:
            self[Name("IC")] = List().set_is_inline(True)
            self["IC"].append(bDecimal(stroke_color.to_rgb().red))
            self["IC"].append(bDecimal(stroke_color.to_rgb().green))
            self["IC"].append(bDecimal(stroke_color.to_rgb().blue))

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
