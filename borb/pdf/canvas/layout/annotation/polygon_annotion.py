#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Polygon annotations (PDF 1.5) display closed polygons on the page. Such polygons may have any number of
vertices connected by straight lines. Polyline annotations (PDF 1.5) are similar to polygons, except that the first
and last vertex are not implicitly connected.
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


class PolygonAnnotation(Annotation):
    """
    Polygon annotations (PDF 1.5) display closed polygons on the page. Such polygons may have any number of
    vertices connected by straight lines. Polyline annotations (PDF 1.5) are similar to polygons, except that the first
    and last vertex are not implicitly connected.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        points: typing.List[typing.Tuple[Decimal, Decimal]],
        stroke_color: Color = HexColor("000000"),
    ):
        # must be at least 3 points
        assert len(points) >= 3

        # bounding box
        min_x = points[0][0]
        min_y = points[0][1]
        max_x = min_x
        max_y = min_y
        for p in points:
            min_x = min(min_x, p[0])
            min_y = min(min_y, p[1])
            max_x = max(max_x, p[0])
            max_y = max(max_y, p[1])

        super(PolygonAnnotation, self).__init__(
            bounding_box=Rectangle(min_x, min_y, max_x - min_x, max_y - min_y),
            color=stroke_color,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Polygon or PolyLine for a polygon or polyline annotation, respectively.
        self[Name("Subtype")] = Name("Polygon")

        # (Required) An array of numbers (see Table 174) specifying the width and
        # dash pattern that shall represent the alternating horizontal and vertical
        # coordinates, respectively, of each vertex, in default user space.
        self[Name("Vertices")] = List().set_is_inline(True)
        for p in points:
            self["Vertices"].append(bDecimal(p[0]))
            self["Vertices"].append(bDecimal(p[1]))

        # (Optional; PDF 1.4) An array of two names specifying the line ending
        # styles that shall be used in drawing the line. The first and second
        # elements of the array shall specify the line ending styles for the endpoints
        # defined, respectively, by the first and second pairs of coordinates, (x 1 , y 1 )
        # and (x 2 , y 2 ), in the L array. Table 176 shows the possible values. Default
        # value: [ /None /None ].
        self[Name("LE")] = List().set_is_inline(True)
        self["LE"].append(Name("None"))
        self["LE"].append(Name("None"))

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
