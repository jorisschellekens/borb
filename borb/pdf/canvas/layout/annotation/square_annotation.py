#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Square and circle annotations (PDF 1.3) shall display, respectively, a rectangle or an ellipse on the page. When
opened, they shall display a pop-up window containing the text of the associated note. The rectangle or ellipse
shall be inscribed within the annotation rectangle defined by the annotation dictionary’s Rect entry (see
Table 168).
"""
import typing
from decimal import Decimal

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class SquareAnnotation(Annotation):
    """
    Square and circle annotations (PDF 1.3) shall display, respectively, a rectangle or an ellipse on the page. When
    opened, they shall display a pop-up window containing the text of the associated note. The rectangle or ellipse
    shall be inscribed within the annotation rectangle defined by the annotation dictionary’s Rect entry (see
    Table 168).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        bounding_box: Rectangle,
        fill_color: typing.Optional[Color] = None,
        rectangle_difference: typing.Optional[
            typing.Tuple[Decimal, Decimal, Decimal, Decimal]
        ] = None,
        stroke_color: typing.Optional[Color] = None,
    ):
        super(SquareAnnotation, self).__init__(
            bounding_box=bounding_box, color=stroke_color
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Square or Circle for a square or circle annotation, respectively.
        self[Name("Subtype")] = Name("Square")

        # (Optional) A border style dictionary (see Table 166) specifying the line
        # width and dash pattern that shall be used in drawing the rectangle or
        # ellipse.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Rect and BS entries; see Table 168 and 12.5.5, “Appearance
        # Streams.”
        # self[Name("BS")] = None

        # (Optional; PDF 1.4) An array of numbers that shall be in the range 0.0 to
        # 1.0 and shall specify the interior color with which to fill the annotation’s
        # rectangle or ellipse. The number of array elements determines the colour
        # space in which the colour shall be defined
        if fill_color is not None:
            self[Name("IC")] = List().set_is_inline(True)
            self["IC"].append(bDecimal(fill_color.to_rgb().red))
            self["IC"].append(bDecimal(fill_color.to_rgb().green))
            self["IC"].append(bDecimal(fill_color.to_rgb().blue))

        # (Optional; PDF 1.5) A border effect dictionary describing an effect applied
        # to the border described by the BS entry (see Table 167).
        # self[Name("BE")] = None

        # (Optional; PDF 1.5) A set of four numbers that shall describe the
        # numerical differences between two rectangles: the Rect entry of the
        # annotation and the actual boundaries of the underlying square or circle.
        # Such a difference may occur in situations where a border effect
        # (described by BE) causes the size of the Rect to increase beyond that of
        # the square or circle.
        # The four numbers shall correspond to the differences in default user
        # space between the left, top, right, and bottom coordinates of Rect and
        # those of the square or circle, respectively. Each value shall be greater
        # than or equal to 0. The sum of the top and bottom differences shall be
        # less than the height of Rect, and the sum of the left and right differences
        # shall be less than the width of Rect.
        if rectangle_difference is not None:
            self[Name("RD")] = List().set_is_inline(True)
            self["RD"].append(bDecimal(rectangle_difference[0]))
            self["RD"].append(bDecimal(rectangle_difference[1]))
            self["RD"].append(bDecimal(rectangle_difference[2]))
            self["RD"].append(bDecimal(rectangle_difference[3]))

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
