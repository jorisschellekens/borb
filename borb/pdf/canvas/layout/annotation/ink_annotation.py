#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An ink annotation (PDF 1.3) represents a freehand “scribble” composed of one or more disjoint paths. When
opened, it shall display a pop-up window containing the text of the associated note. Table 182 shows the
annotation dictionary entries specific to this type of annotation.
"""
import typing
from decimal import Decimal

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import List as bList
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class InkAnnotation(Annotation):
    """
    An ink annotation (PDF 1.3) represents a freehand “scribble” composed of one or more disjoint paths. When
    opened, it shall display a pop-up window containing the text of the associated note. Table 182 shows the
    annotation dictionary entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        points: typing.List[typing.Tuple[Decimal, Decimal]],
        color: typing.Optional[Color] = None,
        line_width: typing.Optional[Decimal] = None,
    ):
        super(InkAnnotation, self).__init__(
            bounding_box=Rectangle(
                min([x for x, y in points]),
                min([y for x, y in points]),
                max([x for x, y in points]) - min([x for x, y in points]),
                max([y for x, y in points]) - min([y for x, y in points]),
            ),
            color=color,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Polygon or PolyLine for a polygon or polyline annotation, respectively.
        self[Name("Subtype")] = Name("Ink")

        # (Required) An array of n arrays, each representing a stroked path. Each
        # array shall be a series of alternating horizontal and vertical coordinates in
        # default user space, specifying points along the path. When drawn, the
        # points shall be connected by straight lines or curves in an
        # implementation-dependent way.
        self[Name("InkList")] = bList().set_is_inline(True)
        self["InkList"].append(bList().set_is_inline(True))
        for p in points:
            self["InkList"][0].append(bDecimal(p[0]))
            self["InkList"][0].append(bDecimal(p[1]))

        # (Optional) A border style dictionary (see Table 166) specifying the line
        # width and dash pattern that shall be used in drawing the paths.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the InkList and BS entries; see Table 168 and 12.5.5, “Appearance
        # Streams.”
        # TODO

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
        if line_width is not None:
            self[Name("Border")] = bList().set_is_inline(True)
            self["Border"].append(bDecimal(0))
            self["Border"].append(bDecimal(0))
            self["Border"].append(bDecimal(line_width))

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
