#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
annotations.
"""
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class UnderlineAnnotation(Annotation):
    """
    Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
    underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
    the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
    annotations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self, bounding_box: Rectangle, stroke_color: Color = HexColor("faed27")
    ):
        super(UnderlineAnnotation, self).__init__(
            bounding_box=bounding_box, color=stroke_color
        )

        # (Required) The type of annotation that this dictionary describes; shall
        # be Underline for a underline annotation.
        self[Name("Subtype")] = Name("Underline")

        # (Required) An array of 8 × n numbers specifying the coordinates of n
        # quadrilaterals in default user space. Each quadrilateral shall
        # encompass a word or group of contiguous words in the text
        # underlying the annotation. The coordinates for each quadrilateral shall
        # be given in the order
        self[Name("QuadPoints")] = List()
        self["QuadPoints"].append(bDecimal(bounding_box.get_x()))
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_y() + bounding_box.get_height())
        )
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_x() + bounding_box.get_width())
        )
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_y() + bounding_box.get_height())
        )
        self["QuadPoints"].append(bDecimal(bounding_box.get_x()))
        self["QuadPoints"].append(bDecimal(bounding_box.get_y()))
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_x() + bounding_box.get_width())
        )
        self["QuadPoints"].append(bDecimal(bounding_box.get_y()))

        # (PDF 1.0) The array consists of three numbers defining the horizontal
        # corner radius, vertical corner radius, and border width, all in default user
        # space units. If the corner radii are 0, the border has square (not rounded)
        # corners; if the border width is 0, no border is drawn.
        self[Name("Border")] = List()
        self["Border"].append(bDecimal(0))
        self["Border"].append(bDecimal(0))
        self["Border"].append(bDecimal(1))

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
