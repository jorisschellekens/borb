#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An annotation associates an object such as a note, sound, or movie with a location on a page of a PDF
document, or provides a way to interact with the user by means of the mouse and keyboard. PDF includes a
wide variety of standard annotation types, described in detail in 12.5.6, “Annotation Types.”
"""
import datetime
import typing
from decimal import Decimal

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import List
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.geometry.rectangle import Rectangle


class Annotation(Dictionary):
    """
    An annotation associates an object such as a note, sound, or movie with a location on a page of a PDF
    document, or provides a way to interact with the user by means of the mouse and keyboard. PDF includes a
    wide variety of standard annotation types, described in detail in 12.5.6, “Annotation Types.”
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        bounding_box: Rectangle,
        border_width: typing.Optional[Decimal] = None,
        color: typing.Optional[Color] = None,
        contents: typing.Optional[str] = None,
        horizontal_corner_radius: typing.Optional[Decimal] = None,
        vertical_corner_radius: typing.Optional[Decimal] = None,
    ):
        super(Annotation, self).__init__()

        # (Optional) The type of PDF object that this dictionary describes; if
        # present, shall be Annot for an annotation dictionary.
        self[Name("Type")] = Name("Annot")

        # (Required) The annotation rectangle, defining the location of the
        # annotation on the page in default user space units.
        self[Name("Rect")] = List().set_is_inline(True)
        self["Rect"].append(bDecimal(bounding_box.get_x()))
        self["Rect"].append(bDecimal(bounding_box.get_y()))
        self["Rect"].append(bDecimal(bounding_box.get_x() + bounding_box.get_width()))
        self["Rect"].append(bDecimal(bounding_box.get_y() + bounding_box.get_height()))

        # (Optional) Text that shall be displayed for the annotation or, if this type of
        # annotation does not display text, an alternate description of the
        # annotation’s contents in human-readable form. In either case, this text is
        # useful when extracting the document’s contents in support of
        # accessibility to users with disabilities or for other purposes (see 14.9.3,
        # “Alternate Descriptions”). See 12.5.6, “Annotation Types” for more
        # details on the meaning of this entry for each annotation type.
        if contents is not None:
            self[Name("Contents")] = String(contents)

        # (Optional; PDF 1.4) The annotation name, a text string uniquely
        # identifying it among all the annotations on its page.
        len_annots: int = 0
        self[Name("NM")] = String("annotation-{0:03d}".format(len_annots))

        # (Optional; PDF 1.1) The date and time when the annotation was most
        # recently modified. The format should be a date string as described in
        # 7.9.4, “Dates,” but conforming readers shall accept and display a string
        # in any format.
        self[Name("M")] = String(self._timestamp_to_str())

        # (Optional; PDF 1.1) A set of flags specifying various characteristics of
        # the annotation (see 12.5.3, “Annotation Flags”). Default value: 0.
        self[Name("F")] = bDecimal(4)

        # (Optional; PDF 1.2) An appearance dictionary specifying how the
        # annotation shall be presented visually on the page (see 12.5.5,
        # “Appearance Streams”). Individual annotation handlers may ignore this
        # entry and provide their own appearances.
        # self[Name("AP")] = None

        # (Required if the appearance dictionary AP contains one or more
        # subdictionaries; PDF 1.2) The annotation’s appearance state, which
        # selects the applicable appearance stream from an appearance
        # subdictionary (see Section 12.5.5, “Appearance Streams”).
        # self[Name("AS")] = None

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
        if (
            horizontal_corner_radius is not None
            and vertical_corner_radius is not None
            and border_width is not None
        ):
            self[Name("Border")] = List().set_is_inline(True)
            self["Border"].append(bDecimal(horizontal_corner_radius))
            self["Border"].append(bDecimal(vertical_corner_radius))
            self["Border"].append(bDecimal(border_width))

        # (Optional; PDF 1.1) An array of numbers in the range 0.0 to 1.0,
        # representing a colour used for the following purposes:
        # The background of the annotation’s icon when closed
        # The title bar of the annotation’s pop-up window
        # The border of a link annotation
        # The number of array elements determines the colour space in which the
        # colour shall be defined
        if color is not None:
            self[Name("C")] = List().set_is_inline(True)
            self["C"].append(bDecimal(color.to_rgb().red))
            self["C"].append(bDecimal(color.to_rgb().green))
            self["C"].append(bDecimal(color.to_rgb().blue))

        # (Required if the annotation is a structural content item; PDF 1.3) The
        # integer key of the annotation’s entry in the structural parent tree (see
        # 14.7.4.4, “Finding Structure Elements from Content Items”)
        # self[Name("StructParent")] = None

        # (Optional; PDF 1.5) An optional content group or optional content
        # membership dictionary (see 8.11, “Optional Content”) specifying the
        # optional content properties for the annotation. Before the annotation is
        # drawn, its visibility shall be determined based on this entry as well as the
        # annotation flags specified in the F entry (see 12.5.3, “Annotation Flags”).
        # If it is determined to be invisible, the annotation shall be skipped, as if it
        # were not in the document.
        # self[Name("OC")] = None

    #
    # PRIVATE
    #

    @staticmethod
    def _timestamp_to_str() -> str:
        timestamp_str = "D:"
        now = datetime.datetime.now()
        for n in [now.year, now.month, now.day, now.hour, now.minute, now.second]:
            timestamp_str += "{0:02}".format(n)
        timestamp_str += "Z00"
        return timestamp_str

    #
    # PUBLIC
    #
