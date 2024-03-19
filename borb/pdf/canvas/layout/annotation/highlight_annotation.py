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


class HighlightAnnotation(Annotation):
    """
    Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
    underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
    the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
    annotations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, bounding_box: Rectangle, color: Color = HexColor("faed27")):
        # create generic annotation
        super(HighlightAnnotation, self).__init__(
            bounding_box=bounding_box, color=color
        )

        # (Required) The type of annotation that this dictionary describes; shall
        # be Highlight, Underline, Squiggly, or StrikeOut for a highlight,
        # underline, squiggly-underline, or strikeout annotation, respectively.
        self[Name("Subtype")] = Name("Highlight")

        # (Required) An array of 8 × n numbers specifying the coordinates of n
        # quadrilaterals in default user space. Each quadrilateral shall
        # encompasses a word or group of contiguous words in the text
        # underlying the annotation. The coordinates for each quadrilateral shall
        # be given in the order
        # x1 y1 x2 y2 x3 y3 x4 y4
        self[Name("QuadPoints")] = List().set_is_inline(True)
        # x1, y1
        self["QuadPoints"].append(bDecimal(bounding_box.get_x()))
        self["QuadPoints"].append(bDecimal(bounding_box.get_y()))
        # x4, y4
        self["QuadPoints"].append(bDecimal(bounding_box.get_x()))
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_y() + bounding_box.get_height())
        )
        # x2, y2
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_x() + bounding_box.get_width())
        )
        self["QuadPoints"].append(bDecimal(bounding_box.get_y()))
        # x3, y3
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_x() + bounding_box.get_width())
        )
        self["QuadPoints"].append(
            bDecimal(bounding_box.get_y() + bounding_box.get_height())
        )

        # border
        self[Name("Border")] = List().set_is_inline(True)
        self["Border"].append(bDecimal(0))
        self["Border"].append(bDecimal(0))
        self["Border"].append(bDecimal(1))

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
