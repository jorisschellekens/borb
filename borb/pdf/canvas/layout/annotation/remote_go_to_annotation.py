#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A link annotation represents either a hypertext link to a destination elsewhere in the document (see 12.3.2,
“Destinations”) or an action to be performed (12.6, “Actions”). Table 173 shows the annotation dictionary
entries specific to this type of annotation.
This method adds a link annotation with an action that opens a remote URI.
"""
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class RemoteGoToAnnotation(Annotation):
    """
    A link annotation represents either a hypertext link to a destination elsewhere in the document (see 12.3.2,
    “Destinations”) or an action to be performed (12.6, “Actions”). Table 173 shows the annotation dictionary
    entries specific to this type of annotation.
    This method adds a link annotation with an action that opens a remote URI.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, bounding_box: Rectangle, uri: str):
        super(RemoteGoToAnnotation, self).__init__(bounding_box)

        # (Required) The type of annotation that this dictionary describes; shall be
        # Link for a link annotation.
        self[Name("Subtype")] = Name("Link")

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
        self[Name("Border")] = List().set_is_inline(True)
        for _ in range(0, 3):
            self[Name("Border")].append(bDecimal(0))

        # (Optional; PDF 1.1) An action that shall be performed when the link
        # annotation is activated (see 12.6, “Actions”).
        self[Name("A")] = Dictionary()
        self["A"][Name("Type")] = Name("Action")
        self["A"][Name("S")] = Name("URI")
        self["A"][Name("URI")] = String(uri)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
