#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class represents a single page in a PDF document
"""
import datetime
import enum
import io
import typing
import zlib
from decimal import Decimal
from typing import Optional, Tuple

from borb.io.read.types import Boolean
from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary, List, Name, Stream, String
from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.color.color import Color, HexColor, X11Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.page.page_info import PageInfo


class RubberStampAnnotationIconType(enum.Enum):
    """
    This Enum represents all possible rubber stamp annotation icons
    """

    APPROVED = Name("Approved")
    AS_IS = Name("AsIs")
    CONFIDENTIAL = Name("Confidential")
    DEPARTMENTAL = Name("Departmental")
    DRAFT = Name("Draft")
    EXPERIMENTAL = Name("Experimental")
    EXPIRED = Name("Expired")
    FINAL = Name("Final")
    FOR_COMMENT = Name("ForComment")
    FOR_PUBLIC_RELEASE = Name("ForPublicRelease")
    NOT_APPROVED = Name("NotApproved")
    NOT_FOR_PUBLIC_RELEASE = Name("NotForPublicRelease")
    SOLD = Name("Sold")
    TOP_SECRET = Name("TopSecret")


class DestinationType(enum.Enum):
    """
    This Enum represents all possible destination types (when adding a link annotation)
    """

    FIT = Name("Fit")
    FIT_B = Name("FitB")
    FIT_B_H = Name("FitBH")
    FIT_B_V = Name("FitBV")
    FIT_H = Name("FitH")
    FIT_R = Name("FitR")
    FIT_V = Name("FitV")
    X_Y_Z = Name("XYZ")


class TextAnnotationIconType(enum.Enum):
    """
    This Enum represents all possible text annotation icon types
    """

    COMMENT = Name("Comment")
    HELP = Name("Help")
    INSERT = Name("Insert")
    KEY = Name("Key")
    NEW_PARAGRAPH = Name("NewParagraph")
    NOTE = Name("Note")
    PARAGRAPH = Name("Paragraph")


class LineEndStyleType(enum.Enum):
    """
    This Enum represents all possible line end styles
    """

    SQUARE = Name("Square")
    CIRCLE = Name("Circle")
    DIAMOND = Name("Diamond")
    OPEN_ARROW = Name("OpenArrow")
    CLOSED_ARROW = Name("ClosedArrow")
    NONE = Name("None")
    BUTT = Name("Butt")
    RIGHT_OPEN_ARROW = Name("ROpenArrow")
    RIGHT_CLOSED_ARROW = Name("RClosedArrow")
    SLASH = Name("Slash")


class Page(Dictionary):
    """
    This class represents a single page in a PDF document
    """

    def __init__(self, width: Decimal = Decimal(595), height: Decimal = Decimal(842)):
        super(Page, self).__init__()

        # type
        self[Name("Type")] = Name("Page")

        # size: A4 portrait
        self[Name("MediaBox")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        self["MediaBox"].append(bDecimal(0))
        self["MediaBox"].append(bDecimal(0))
        self["MediaBox"].append(bDecimal(width))
        self["MediaBox"].append(bDecimal(height))

    def get_page_info(self) -> PageInfo:
        """
        This function returns the PageInfo object for this Page
        """
        return PageInfo(self)

    def get_document(self) -> "Document":  # type: ignore [name-defined]
        """
        This function returns the Document from which this Page came
        """
        return self.get_root()  # type: ignore [attr-defined]

    #
    # FORMS
    #

    def has_acroforms(self) -> bool:
        """
        This function returns True if this Page contains fields from an AcroForm
        :return:    True if this Page contains fields from an AcroForm, False otherwise
        """
        return (
            len(
                [
                    x
                    for x in self.get("Annots", [])
                    if "Type" in x
                    and x["Type"] == "Annot"
                    and "Subtype" in x
                    and x["Subtype"] == "Widget"
                    and "FT" in x
                    and x["FT"] in ["Btn", "Ch", "Tx"]
                ]
            )
            != 0
        )

    def has_form_field(self, field_name: str) -> bool:
        """
        This function returns True if this Page contains a form field with the given name
        :param field_name:  the field_name to be queried
        :return:            True if this Page contains a form field with the given field_name
        """
        assert len(field_name) != 0
        return (
            len(
                [
                    x
                    for x in self.get("Annots", [])
                    if "Type" in x
                    and x["Type"] == "Annot"
                    and "Subtype" in x
                    and x["Subtype"] == "Widget"
                    and "FT" in x
                    and x["FT"] in ["Btn", "Ch", "Tx"]
                    and "T" in x
                    and x["T"] == field_name
                ]
            )
            != 0
        )

    def get_form_field_value(
        self, field_name: str
    ) -> typing.Optional[typing.Union[str, bool]]:
        """
        This function returns the value of the form field with the given field_name
        :param field_name:  the field_name of the field to be queried
        :return:            the value of the form field being queried
        """
        field_dictionaries: typing.List[Dictionary] = [
            x
            for x in self.get("Annots", [])
            if "Type" in x
            and x["Type"] == "Annot"
            and "Subtype" in x
            and x["Subtype"] == "Widget"
            and "FT" in x
            and x["FT"] in ["Btn", "Ch", "Tx"]
            and "T" in x
            and x["T"] == field_name
        ]
        assert len(field_dictionaries) == 1
        assert "V" in field_dictionaries[0]
        return field_dictionaries[0]["V"]

    def set_form_field_value(self, field_name: str, value: str) -> "Page":
        """
        This function sets the value of the form field with the given field_name
        This function returns self
        :param field_name:  the field_name of the field being queried
        :param value:       the new value of the field
        :return:            self
        """
        field_dictionaries: typing.List[Dictionary] = [
            x
            for x in self.get("Annots", [])
            if "Type" in x
            and x["Type"] == "Annot"
            and "Subtype" in x
            and x["Subtype"] == "Widget"
            and "FT" in x
            and x["FT"] in ["Btn", "Ch", "Tx"]
            and "T" in x
            and x["T"] == field_name
        ]
        assert len(field_dictionaries) == 1
        assert "V" in field_dictionaries[0]
        field_dictionaries[0][Name("V")] = String(value)
        return self

    #
    # ROTATE
    #

    def rotate_right(self) -> "Page":
        """
        This function rotates the Page clockwise by 90 degrees.
        This function returns self.
        """
        # get current rotation
        angle: int = 0
        if "Rotate" in self:
            angle = int(self["Rotate"])

        # rotate left
        angle = (angle + 90) % 360

        # write entry
        if angle == 0 and "Rotate" in self:
            self.pop("Rotate")
        else:
            self[Name("Rotate")] = bDecimal(angle)

        # return
        return self

    def rotate_left(self) -> "Page":
        """
        This function rotates the Page counterclockwise by 90 degrees.
        This function returns self.
        """

        # get current rotation
        angle: int = 0
        if "Rotate" in self:
            angle = int(self["Rotate"])

        # rotate left
        angle = (angle + 270) % 360

        # write entry
        if angle == 0 and "Rotate" in self:
            self.pop("Rotate")
        else:
            self[Name("Rotate")] = bDecimal(angle)

        # return
        return self

    #
    # ANNOTATIONS
    #

    def get_annotations(self) -> List:
        """
        This function returns the annotation(s) on this Page
        """
        if "Annots" not in self:
            self[Name("Annots")] = List()
        return self["Annots"]

    def _create_annotation(
        self,
        rectangle: Rectangle,
        contents: Optional[str] = None,
        color: Optional[Color] = None,
        border_horizontal_corner_radius: Optional[Decimal] = None,
        border_vertical_corner_radius: Optional[Decimal] = None,
        border_width: Optional[Decimal] = None,
    ):
        annot = Dictionary()

        # (Optional) The type of PDF object that this dictionary describes; if
        # present, shall be Annot for an annotation dictionary.
        annot[Name("Type")] = Name("Annot")

        # (Required) The annotation rectangle, defining the location of the
        # annotation on the page in default user space units.
        annot[Name("Rect")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["Rect"].append(bDecimal(rectangle.get_x()))
        annot["Rect"].append(bDecimal(rectangle.get_y()))
        annot["Rect"].append(bDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["Rect"].append(bDecimal(rectangle.get_y() + rectangle.get_height()))

        # (Optional) Text that shall be displayed for the annotation or, if this type of
        # annotation does not display text, an alternate description of the
        # annotation’s contents in human-readable form. In either case, this text is
        # useful when extracting the document’s contents in support of
        # accessibility to users with disabilities or for other purposes (see 14.9.3,
        # “Alternate Descriptions”). See 12.5.6, “Annotation Types” for more
        # details on the meaning of this entry for each annotation type.
        if contents is not None:
            annot[Name("Contents")] = String(contents)

        # (Optional except as noted below; PDF 1.3; not used in FDF files) An
        # indirect reference to the page object with which this annotation is
        # associated.
        # This entry shall be present in screen annotations associated with
        # rendition actions (PDF 1.5; see 12.5.6.18, “Screen Annotations” and
        # 12.6.4.13, “Rendition Actions”).
        annot[Name("P")] = self

        # (Optional; PDF 1.4) The annotation name, a text string uniquely
        # identifying it among all the annotations on its page.
        len_annots = len(self["Annots"]) if "Annots" in self else 0
        annot[Name("NM")] = String("annotation-{0:03d}".format(len_annots))

        # (Optional; PDF 1.1) The date and time when the annotation was most
        # recently modified. The format should be a date string as described in
        # 7.9.4, “Dates,” but conforming readers shall accept and display a string
        # in any format.
        annot[Name("M")] = String(self._timestamp_to_str())

        # (Optional; PDF 1.1) A set of flags specifying various characteristics of
        # the annotation (see 12.5.3, “Annotation Flags”). Default value: 0.
        annot[Name("F")] = bDecimal(4)

        # (Optional; PDF 1.2) An appearance dictionary specifying how the
        # annotation shall be presented visually on the page (see 12.5.5,
        # “Appearance Streams”). Individual annotation handlers may ignore this
        # entry and provide their own appearances.
        # annot[Name("AP")] = None

        # (Required if the appearance dictionary AP contains one or more
        # subdictionaries; PDF 1.2) The annotation’s appearance state, which
        # selects the applicable appearance stream from an appearance
        # subdictionary (see Section 12.5.5, “Appearance Streams”).
        # annot[Name("AS")] = None

        # Optional) An array specifying the characteristics of the annotation’s
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
            border_horizontal_corner_radius is not None
            and border_vertical_corner_radius is not None
            and border_width is not None
        ):
            annot[Name("Border")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["Border"].append(bDecimal(border_horizontal_corner_radius))
            annot["Border"].append(bDecimal(border_vertical_corner_radius))
            annot["Border"].append(bDecimal(border_width))

        # (Optional; PDF 1.1) An array of numbers in the range 0.0 to 1.0,
        # representing a colour used for the following purposes:
        # The background of the annotation’s icon when closed
        # The title bar of the annotation’s pop-up window
        # The border of a link annotation
        # The number of array elements determines the colour space in which the
        # colour shall be defined
        if color is not None:
            annot[Name("C")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["C"].append(bDecimal(color.to_rgb().red))
            annot["C"].append(bDecimal(color.to_rgb().green))
            annot["C"].append(bDecimal(color.to_rgb().blue))

        # (Required if the annotation is a structural content item; PDF 1.3) The
        # integer key of the annotation’s entry in the structural parent tree (see
        # 14.7.4.4, “Finding Structure Elements from Content Items”)
        # annot[Name("StructParent")] = None

        # (Optional; PDF 1.5) An optional content group or optional content
        # membership dictionary (see 8.11, “Optional Content”) specifying the
        # optional content properties for the annotation. Before the annotation is
        # drawn, its visibility shall be determined based on this entry as well as the
        # annotation flags specified in the F entry (see 12.5.3, “Annotation Flags”).
        # If it is determined to be invisible, the annotation shall be skipped, as if it
        # were not in the document.
        # annot[Name("OC")] = None

        # return
        return annot

    @staticmethod
    def _timestamp_to_str() -> str:
        timestamp_str = "D:"
        now = datetime.datetime.now()
        for n in [now.year, now.month, now.day, now.hour, now.minute, now.second]:
            timestamp_str += "{0:02}".format(n)
        timestamp_str += "Z00"
        return timestamp_str

    def _append_annotation(self, annotation: Dictionary) -> "Page":
        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
            self["Annots"].set_parent(self)
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annotation)
        return self

    def append_text_annotation(
        self,
        rectangle: Rectangle,
        contents: str,
        text_annotation_icon: TextAnnotationIconType,
        open: Optional[bool] = None,
        color: Optional[Color] = None,
    ) -> "Page":
        """
        A text annotation represents a “sticky note” attached to a point in the PDF document. When closed, the
        annotation shall appear as an icon; when open, it shall display a pop-up window containing the text of the note
        in a font and size chosen by the conforming reader. Text annotations shall not scale and rotate with the page;
        they shall behave as if the NoZoom and NoRotate annotation flags (see Table 165) were always set. Table 172
        shows the annotation dictionary entries specific to this type of annotation.
        """
        # create generic annotation
        annot = self._create_annotation(
            rectangle=rectangle, contents=contents, color=color
        )

        # specific for text annotations
        annot[Name("Subtype")] = Name("Text")

        # (Optional) A flag specifying whether the annotation shall initially be
        # displayed open. Default value: false (closed).
        if open is not None:
            annot[Name("Open")] = Boolean(open)

        # (Optional) The name of an icon that shall be used in displaying the
        # annotation. Conforming readers shall provide predefined icon
        # appearances for at least the following standard names:
        # Comment, Key, Note, Help, NewParagraph, Paragraph, Insert
        # Additional names may be supported as well. Default value: Note.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Name entry; see Table 168 and 12.5.5, “Appearance Streams.”
        annot[Name("Name")] = text_annotation_icon.value

        # return
        return self._append_annotation(annot)

    def append_link_annotation(
        self,
        rectangle: Rectangle,
        page: Decimal,
        destination_type: DestinationType,
        top: Optional[Decimal] = None,
        right: Optional[Decimal] = None,
        bottom: Optional[Decimal] = None,
        left: Optional[Decimal] = None,
        zoom: Optional[Decimal] = None,
        highlighting_mode: Optional[str] = None,
        color: Optional[Color] = None,
    ) -> "Page":
        """
        A link annotation represents either a hypertext link to a destination elsewhere in the document (see 12.3.2,
        “Destinations”) or an action to be performed (12.6, “Actions”). Table 173 shows the annotation dictionary
        entries specific to this type of annotation.
        """

        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle, color=color)

        # specific for text annotations
        annot[Name("Subtype")] = Name("Link")

        # (Optional; PDF 1.1) An action that shall be performed when the link
        # annotation is activated (see 12.6, “Actions”).
        # annot[Name("A")] = None

        # (Optional; not permitted if an A entry is present) A destination that shall
        # be displayed when the annotation is activated (see 12.3.2,
        # “Destinations”).
        destination = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        destination.append(bDecimal(page))
        destination.append(destination_type.value)
        if destination_type == DestinationType.X_Y_Z:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is not None
                and zoom is not None
            )
            destination.append(bDecimal(left))
            destination.append(bDecimal(top))
            destination.append(bDecimal(zoom))
        if destination_type == DestinationType.FIT:
            assert (
                left is None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
        if destination_type == DestinationType.FIT_H:
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(bDecimal(top))
        if destination_type == DestinationType.FIT_V:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(bDecimal(left))
        if destination_type == DestinationType.FIT_R:
            assert (
                left is not None
                and bottom is not None
                and right is not None
                and top is not None
                and zoom is None
            )
            destination.append(bDecimal(left))
            destination.append(bDecimal(bottom))
            destination.append(bDecimal(right))
            destination.append(bDecimal(top))
        if destination_type == DestinationType.FIT_B_H:
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(bDecimal(top))
        if destination_type == DestinationType.FIT_B_V:
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(bDecimal(left))
        annot[Name("Dest")] = destination

        # (Optional; PDF 1.2) The annotation’s highlighting mode, the visual effect
        # that shall be used when the mouse button is pressed or held down
        # inside its active area:
        # N     (None) No highlighting.
        # I     (Invert) Invert the contents of the annotation rectangle.
        # O     (Outline) Invert the annotation’s border.
        # P     (Push) Display the annotation as if it were being pushed below the surface of the page.
        if highlighting_mode is not None:
            assert highlighting_mode in ["N", "I", "O", "P"]
            annot[Name("H")] = String(highlighting_mode)

        # return
        return self._append_annotation(annot)

    def append_remote_go_to_annotation(
        self,
        rectangle: Rectangle,
        uri: str,
        border_horizontal_corner_radius: Decimal = Decimal(0),
        border_vertical_corner_radius: Decimal = Decimal(0),
        border_width: Decimal = Decimal(0),
    ):
        """
        A link annotation represents either a hypertext link to a destination elsewhere in the document (see 12.3.2,
        “Destinations”) or an action to be performed (12.6, “Actions”). Table 173 shows the annotation dictionary
        entries specific to this type of annotation.
        This method adds a link annotation with an action that opens a remote URI.
        """
        annot: Dictionary = self._create_annotation(
            rectangle=rectangle,
            border_horizontal_corner_radius=bDecimal(border_horizontal_corner_radius),
            border_vertical_corner_radius=bDecimal(border_vertical_corner_radius),
            border_width=bDecimal(border_width),
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Link for a link annotation.
        annot[Name("Subtype")] = Name("Link")

        # (Optional; PDF 1.1) An action that shall be performed when the link
        # annotation is activated (see 12.6, “Actions”).
        annot[Name("A")] = Dictionary()
        annot["A"][Name("Type")] = Name("Action")
        annot["A"][Name("S")] = Name("URI")
        annot["A"][Name("URI")] = String(uri)

        # return
        return self._append_annotation(annot)

    def append_free_text_annotation(
        self,
        rectangle: Rectangle,
        font: "Font",  # type: ignore [name-defined]
        font_size: Decimal,
        font_color: "Color",  # type: ignore [name-defined]
        text: str,
        background_color: "Color" = HexColor("ffffff"),
        border_horizontal_corner_radius: Decimal = Decimal(0),
        border_vertical_corner_radius: Decimal = Decimal(0),
        border_width: Decimal = Decimal(0),
    ) -> "Page":
        """
        A free text annotation (PDF 1.3) displays text directly on the page. Unlike an ordinary text annotation (see
        12.5.6.4, “Text Annotations”), a free text annotation has no open or closed state; instead of being displayed in a
        pop-up window, the text shall be always visible. Table 174 shows the annotation dictionary entries specific to
        this type of annotation. 12.7.3.3, “Variable Text” describes the process of using these entries to generate the
        appearance of the text in these annotations.
        """
        # create generic annotation
        annot = self._create_annotation(
            rectangle=rectangle,
            contents=text,
            color=background_color,
            border_horizontal_corner_radius=bDecimal(border_horizontal_corner_radius),
            border_vertical_corner_radius=bDecimal(border_vertical_corner_radius),
            border_width=bDecimal(border_width),
        )

        # specific for text annotations
        annot[Name("Subtype")] = Name("FreeText")

        # (Optional; PDF 1.1) A set of flags specifying various characteristics of
        # the annotation (see 12.5.3, “Annotation Flags”). Default value: 0.
        annot[Name("F")] = bDecimal(20)

        # embed Font in /Page /Resources /Font
        if "Resources" not in self:
            self[Name("Resources")] = Dictionary()
        if "Font" not in self["Resources"]:
            self["Resources"][Name("Font")] = Dictionary()
        font_number: int = len(self["Resources"]["Font"])
        font_name: str = "F%d" % font_number
        while font_name in self["Resources"]["Font"]:
            font_number += 1
            font_name = "F%d" % font_number
        self["Resources"]["Font"][Name(font_name)] = font

        # (Required) The default appearance string that shall be used in formatting
        # the text (see 12.7.3.3, “Variable Text”).
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the DA entry; see Table 168 and 12.5.5, “Appearance Streams.”
        font_color_rgb: "RGBColor" = font_color.to_rgb()  # type: ignore [name-defined]
        annot[Name("DA")] = String(
            "/%s %f Tf %f %f %f rg"
            % (
                font_name,
                font_size,
                font_color_rgb.red,
                font_color_rgb.green,
                font_color_rgb.blue,
            )
        )

        # (Optional; PDF 1.4) A code specifying the form of quadding (justification)
        # that shall be used in displaying the annotation’s text:
        # 0 Left-justified
        # 1 Centered
        # 2 Right-justified
        # Default value: 0 (left-justified).
        annot[Name("Q")] = bDecimal(0)

        # (Optional; PDF 1.6) A name describing the intent of the free text
        # annotation (see also the IT entry in Table 170). The following values shall
        # be valid:
        # FreeText
        # The annotation is intended to function as a plain
        # free-text annotation. A plain free-text annotation
        # is also known as a text box comment.
        # FreeTextCallout
        # The annotation is intended to function as a
        # callout. The callout is associated with an area on
        # the page through the callout line specified in CL.
        # FreeTextTypeWriter
        # The annotation is intended to function as a click-
        # to-type or typewriter object and no callout line is
        # drawn.
        # Default value: FreeText
        annot[Name("IT")] = Name("FreeTextTypeWriter")

        # return
        return self._append_annotation(annot)

    def append_line_annotation(
        self,
        start_point: Tuple[Decimal, Decimal],
        end_point: Tuple[Decimal, Decimal],
        left_line_end_style: LineEndStyleType = LineEndStyleType.NONE,
        right_line_end_style: LineEndStyleType = LineEndStyleType.NONE,
        stroke_color: Color = HexColor("000000"),
    ) -> "Page":
        """
        The purpose of a line annotation (PDF 1.3) is to display a single straight line on the page. When opened, it shall
        display a pop-up window containing the text of the associated note. Table 175 shows the annotation dictionary
        entries specific to this type of annotation.
        """

        x = min([start_point[0], end_point[0]])
        y = min([start_point[1], end_point[1]])
        w = max([start_point[0], end_point[0]]) - x
        h = max([start_point[1], end_point[1]]) - y

        # create generic annotation
        annot = self._create_annotation(
            rectangle=Rectangle(x, y, w, h), color=stroke_color
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Line for a line annotation.
        annot[Name("Subtype")] = Name("Line")

        # (Required) An array of four numbers, [ x 1 y 1 x 2 y 2 ], specifying the
        # starting and ending coordinates of the line in default user space.
        # If the LL entry is present, this value shall represent the endpoints of the
        # leader lines rather than the endpoints of the line itself; see Figure 60.
        annot[Name("L")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["L"].append(start_point[0])
        annot["L"].append(start_point[1])
        annot["L"].append(end_point[0])
        annot["L"].append(end_point[1])

        # (Optional; PDF 1.4) An array of two names specifying the line ending
        # styles that shall be used in drawing the line. The first and second
        # elements of the array shall specify the line ending styles for the endpoints
        # defined, respectively, by the first and second pairs of coordinates, (x 1 , y 1 )
        # and (x 2 , y 2 ), in the L array. Table 176 shows the possible values. Default
        # value: [ /None /None ].
        annot[Name("LE")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["LE"].append(left_line_end_style.value)
        annot["LE"].append(right_line_end_style)

        # (Optional; PDF 1.4) An array of numbers that shall be in the range 0.0 to
        # 1.0 and shall specify the interior color with which to fill the annotation’s
        # rectangle or ellipse. The number of array elements determines the colour
        # space in which the colour shall be defined
        if stroke_color is not None:
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(bDecimal(stroke_color.to_rgb().red))
            annot["IC"].append(bDecimal(stroke_color.to_rgb().green))
            annot["IC"].append(bDecimal(stroke_color.to_rgb().blue))

        # return
        return self._append_annotation(annot)

    def append_square_annotation(
        self,
        rectangle: Rectangle,
        stroke_color: Color,
        fill_color: Optional[Color] = None,
        rectangle_difference: Optional[
            Tuple[Decimal, Decimal, Decimal, Decimal]
        ] = None,
    ) -> "Page":
        """
        Square and circle annotations (PDF 1.3) shall display, respectively, a rectangle or an ellipse on the page. When
        opened, they shall display a pop-up window containing the text of the associated note. The rectangle or ellipse
        shall be inscribed within the annotation rectangle defined by the annotation dictionary’s Rect entry (see
        Table 168).
        """

        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle, color=stroke_color)

        # (Required) The type of annotation that this dictionary describes; shall be
        # Square or Circle for a square or circle annotation, respectively.
        annot[Name("Subtype")] = Name("Square")

        # (Optional) A border style dictionary (see Table 166) specifying the line
        # width and dash pattern that shall be used in drawing the rectangle or
        # ellipse.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Rect and BS entries; see Table 168 and 12.5.5, “Appearance
        # Streams.”
        # annot[Name("BS")] = None

        # (Optional; PDF 1.4) An array of numbers that shall be in the range 0.0 to
        # 1.0 and shall specify the interior color with which to fill the annotation’s
        # rectangle or ellipse. The number of array elements determines the colour
        # space in which the colour shall be defined
        if fill_color is not None:
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(bDecimal(fill_color.to_rgb().red))
            annot["IC"].append(bDecimal(fill_color.to_rgb().green))
            annot["IC"].append(bDecimal(fill_color.to_rgb().blue))

        # (Optional; PDF 1.5) A border effect dictionary describing an effect applied
        # to the border described by the BS entry (see Table 167).
        # annot[Name("BE")] = None

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
            annot[Name("RD")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["RD"].append(bDecimal(rectangle_difference[0]))
            annot["RD"].append(bDecimal(rectangle_difference[1]))
            annot["RD"].append(bDecimal(rectangle_difference[2]))
            annot["RD"].append(bDecimal(rectangle_difference[3]))

        # return
        return self._append_annotation(annot)

    def append_circle_annotation(
        self,
        rectangle: Rectangle,
        stroke_color: Color,
        rectangle_difference: Optional[
            Tuple[Decimal, Decimal, Decimal, Decimal]
        ] = None,
        fill_color: Optional[Color] = None,
    ) -> "Page":
        """
        Square and circle annotations (PDF 1.3) shall display, respectively, a rectangle or an ellipse on the page. When
        opened, they shall display a pop-up window containing the text of the associated note. The rectangle or ellipse
        shall be inscribed within the annotation rectangle defined by the annotation dictionary’s Rect entry (see
        Table 168).
        """

        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle, color=stroke_color)

        # (Required) The type of annotation that this dictionary describes; shall be
        # Square or Circle for a square or circle annotation, respectively.
        annot[Name("Subtype")] = Name("Circle")

        # (Optional) A border style dictionary (see Table 166) specifying the line
        # width and dash pattern that shall be used in drawing the rectangle or
        # ellipse.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Rect and BS entries; see Table 168 and 12.5.5, “Appearance
        # Streams.”
        # annot[Name("BS")] = None

        # (Optional; PDF 1.4) An array of numbers that shall be in the range 0.0 to
        # 1.0 and shall specify the interior color with which to fill the annotation’s
        # rectangle or ellipse. The number of array elements determines the colour
        # space in which the colour shall be defined
        if fill_color is not None:
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(bDecimal(fill_color.to_rgb().red))
            annot["IC"].append(bDecimal(fill_color.to_rgb().green))
            annot["IC"].append(bDecimal(fill_color.to_rgb().blue))

        # (Optional; PDF 1.5) A border effect dictionary describing an effect applied
        # to the border described by the BS entry (see Table 167).
        # annot[Name("BE")] = None

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
            annot[Name("RD")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["RD"].append(bDecimal(rectangle_difference[0]))
            annot["RD"].append(bDecimal(rectangle_difference[1]))
            annot["RD"].append(bDecimal(rectangle_difference[2]))
            annot["RD"].append(bDecimal(rectangle_difference[3]))

        # return
        return self._append_annotation(annot)

    def append_polygon_annotation(
        self,
        points: typing.List[Tuple[Decimal, Decimal]],
        stroke_color: Color,
        contents: Optional[str] = None,
    ) -> "Page":
        """
        Polygon annotations (PDF 1.5) display closed polygons on the page. Such polygons may have any number of
        vertices connected by straight lines. Polyline annotations (PDF 1.5) are similar to polygons, except that the first
        and last vertex are not implicitly connected.
        """

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

        # create generic annotation
        annot = self._create_annotation(
            rectangle=Rectangle(min_x, min_y, max_x - min_x, max_y - min_y),
            color=stroke_color,
            contents=contents,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Polygon or PolyLine for a polygon or polyline annotation, respectively.
        annot[Name("Subtype")] = Name("Polygon")

        # (Required) An array of numbers (see Table 174) specifying the width and
        # dash pattern that shall represent the alternating horizontal and vertical
        # coordinates, respectively, of each vertex, in default user space.
        annot[Name("Vertices")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        for p in points:
            annot["Vertices"].append(bDecimal(p[0]))
            annot["Vertices"].append(bDecimal(p[1]))

        # (Optional; PDF 1.4) An array of two names specifying the line ending
        # styles that shall be used in drawing the line. The first and second
        # elements of the array shall specify the line ending styles for the endpoints
        # defined, respectively, by the first and second pairs of coordinates, (x 1 , y 1 )
        # and (x 2 , y 2 ), in the L array. Table 176 shows the possible values. Default
        # value: [ /None /None ].
        annot[Name("LE")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["LE"].append(Name("None"))
        annot["LE"].append(Name("None"))

        # return
        return self._append_annotation(annot)

    def append_polyline_annotation(
        self,
        points: typing.List[Tuple[Decimal, Decimal]],
        stroke_color: Color,
        left_line_end_style: LineEndStyleType = LineEndStyleType.NONE,
        right_line_end_style: LineEndStyleType = LineEndStyleType.NONE,
        fill_color: Optional[Color] = None,
        contents: Optional[str] = None,
    ) -> "Page":
        """
        Polygon annotations (PDF 1.5) display closed polygons on the page. Such polygons may have any number of
        vertices connected by straight lines. Polyline annotations (PDF 1.5) are similar to polygons, except that the first
        and last vertex are not implicitly connected.
        """

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

        # create generic annotation
        annot = self._create_annotation(
            rectangle=Rectangle(min_x, min_y, max_x - min_x, max_y - min_y),
            color=stroke_color,
            contents=contents,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Polygon or PolyLine for a polygon or polyline annotation, respectively.
        annot[Name("Subtype")] = Name("PolyLine")

        # (Required) An array of numbers (see Table 174) specifying the width and
        # dash pattern that shall represent the alternating horizontal and vertical
        # coordinates, respectively, of each vertex, in default user space.
        annot[Name("Vertices")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        for p in points:
            annot["Vertices"].append(bDecimal(p[0]))
            annot["Vertices"].append(bDecimal(p[1]))

        # (Optional; PDF 1.4) An array of two names specifying the line ending
        # styles that shall be used in drawing the line. The first and second
        # elements of the array shall specify the line ending styles for the endpoints
        # defined, respectively, by the first and second pairs of coordinates, (x 1 , y 1 )
        # and (x 2 , y 2 ), in the L array. Table 176 shows the possible values. Default
        # value: [ /None /None ].
        annot[Name("LE")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["LE"].append(left_line_end_style)
        annot["LE"].append(right_line_end_style)

        if fill_color is not None:
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(bDecimal(fill_color.to_rgb().red))
            annot["IC"].append(bDecimal(fill_color.to_rgb().green))
            annot["IC"].append(bDecimal(fill_color.to_rgb().blue))

        # return
        return self._append_annotation(annot)

    def append_highlight_annotation(
        self,
        rectangle: Rectangle,
        color: Color = X11Color("Yellow"),
        contents: Optional[str] = None,
    ) -> "Page":
        """
        Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
        underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
        the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
        annotations.
        """
        # create generic annotation
        annot = self._create_annotation(
            rectangle=rectangle, color=color, contents=contents
        )

        # (Required) The type of annotation that this dictionary describes; shall
        # be Highlight, Underline, Squiggly, or StrikeOut for a highlight,
        # underline, squiggly-underline, or strikeout annotation, respectively.
        annot[Name("Subtype")] = Name("Highlight")

        # (Required) An array of 8 × n numbers specifying the coordinates of n
        # quadrilaterals in default user space. Each quadrilateral shall
        # encompasses a word or group of contiguous words in the text
        # underlying the annotation. The coordinates for each quadrilateral shall
        # be given in the order
        # x1 y1 x2 y2 x3 y3 x4 y4
        annot[Name("QuadPoints")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        # x1, y1
        annot["QuadPoints"].append(bDecimal(rectangle.get_x()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y()))
        # x4, y4
        annot["QuadPoints"].append(bDecimal(rectangle.get_x()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y() + rectangle.get_height()))
        # x2, y2
        annot["QuadPoints"].append(bDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y()))
        # x3, y3
        annot["QuadPoints"].append(bDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y() + rectangle.get_height()))

        # border
        annot[Name("Border")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["Border"].append(bDecimal(0))
        annot["Border"].append(bDecimal(0))
        annot["Border"].append(bDecimal(1))

        # return
        return self._append_annotation(annot)

    def append_underline_annotation(
        self,
        rectangle: Rectangle,
        stroke_color: Color = X11Color("Yellow"),
        contents: Optional[str] = None,
    ) -> "Page":
        """
        Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
        underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
        the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
        annotations.
        """
        # create generic annotation
        annot = self._create_annotation(
            rectangle=rectangle, color=stroke_color, contents=contents
        )

        # (Required) The type of annotation that this dictionary describes; shall
        # be Redact for a redaction annotation.
        annot[Name("Subtype")] = Name("Underline")

        # (Required) An array of 8 × n numbers specifying the coordinates of n
        # quadrilaterals in default user space. Each quadrilateral shall
        # encompasses a word or group of contiguous words in the text
        # underlying the annotation. The coordinates for each quadrilateral shall
        # be given in the order
        annot[Name("QuadPoints")] = List()
        annot["QuadPoints"].append(bDecimal(rectangle.get_x()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y() + rectangle.get_height()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y() + rectangle.get_height()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_x()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["QuadPoints"].append(bDecimal(rectangle.get_y()))

        # (PDF 1.0) The array consists of three numbers defining the horizontal
        # corner radius, vertical corner radius, and border width, all in default user
        # space units. If the corner radii are 0, the border has square (not rounded)
        # corners; if the border width is 0, no border is drawn.
        annot[Name("Border")] = List()
        annot["Border"].append(bDecimal(0))
        annot["Border"].append(bDecimal(0))
        annot["Border"].append(bDecimal(1))

        # return
        return self._append_annotation(annot)

    def append_squiggly_annotation(
        self,
        rectangle: Rectangle,
        stroke_color: Color = X11Color("Red"),
        line_width: Decimal = Decimal(1),
    ) -> "Page":
        """
        Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
        underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
        the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
        annotations.
        """

        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle)

        # (Required) The type of annotation that this dictionary describes; shall
        # be Redact for a redaction annotation.
        annot[Name("Subtype")] = Name("Squiggly")

        # (Optional; PDF 1.2) An appearance dictionary specifying how the
        # annotation shall be presented visually on the page (see 12.5.5,
        # “Appearance Streams”). Individual annotation handlers may ignore this
        # entry and provide their own appearances.
        annot[Name("AP")] = Dictionary()
        annot["AP"][Name("N")] = Stream()
        annot["AP"]["N"][Name("Type")] = Name("XObject")
        annot["AP"]["N"][Name("Subtype")] = Name("Form")

        appearance_stream_content = "q %f %f %f RG %f w 0 0 m " % (
            stroke_color.to_rgb().red,
            stroke_color.to_rgb().green,
            stroke_color.to_rgb().blue,
            line_width,
        )
        for x in range(0, int(rectangle.width), 5):
            appearance_stream_content += "%f %f l %f %f l " % (x, 0, x + 2.5, 7)
        appearance_stream_content += "%f %f l " % (
            rectangle.width - rectangle.width % 5 + 5,
            0,
        )
        appearance_stream_content += "S Q"
        annot["AP"]["N"][Name("DecodedBytes")] = bytes(
            appearance_stream_content, "latin1"
        )
        annot["AP"]["N"][Name("Bytes")] = zlib.compress(
            annot["AP"]["N"][Name("DecodedBytes")]
        )
        annot["AP"]["N"][Name("Length")] = bDecimal(
            len(annot["AP"]["N"][Name("Bytes")])
        )
        annot["AP"]["N"][Name("Filter")] = Name("FlateDecode")

        # The lower-left corner of the bounding box (BBox) is set to coordinates (0, 0) in the form coordinate system.
        # The box’s top and right coordinates are taken from the dimensions of the annotation rectangle (the Rect
        # entry in the widget annotation dictionary).
        annot["AP"]["N"][Name("BBox")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["AP"]["N"]["BBox"].append(bDecimal(0))
        annot["AP"]["N"]["BBox"].append(bDecimal(0))
        annot["AP"]["N"]["BBox"].append(bDecimal(rectangle.width))
        annot["AP"]["N"]["BBox"].append(bDecimal(100))

        # return
        return self._append_annotation(annot)

    def append_strike_out_annotation(
        self,
        rectangle: Rectangle,
        stroke_color: Color = X11Color("Red"),
        line_width: Decimal = Decimal(1),
    ) -> "Page":
        """
        Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
        underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
        the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
        annotations.
        """
        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle)

        # (Required) The type of annotation that this dictionary describes; shall
        # be Redact for a redaction annotation.
        annot[Name("Subtype")] = Name("StrikeOut")

        # (Optional; PDF 1.2) An appearance dictionary specifying how the
        # annotation shall be presented visually on the page (see 12.5.5,
        # “Appearance Streams”). Individual annotation handlers may ignore this
        # entry and provide their own appearances.
        annot[Name("AP")] = Dictionary()
        annot["AP"][Name("N")] = Stream()
        annot["AP"]["N"][Name("Type")] = Name("XObject")
        annot["AP"]["N"][Name("Subtype")] = Name("Form")

        appearance_stream_content = "q %f %f %f RG %f w 0 40 m %f 40 l S Q" % (
            stroke_color.to_rgb().red,
            stroke_color.to_rgb().green,
            stroke_color.to_rgb().blue,
            line_width,
            rectangle.width,
        )
        annot["AP"]["N"][Name("DecodedBytes")] = bytes(
            appearance_stream_content, "latin1"
        )
        annot["AP"]["N"][Name("Bytes")] = zlib.compress(
            annot["AP"]["N"][Name("DecodedBytes")]
        )
        annot["AP"]["N"][Name("Length")] = bDecimal(
            len(annot["AP"]["N"][Name("Bytes")])
        )
        annot["AP"]["N"][Name("Filter")] = Name("FlateDecode")

        # The lower-left corner of the bounding box (BBox) is set to coordinates (0, 0) in the form coordinate system.
        # The box’s top and right coordinates are taken from the dimensions of the annotation rectangle (the Rect
        # entry in the widget annotation dictionary).
        annot["AP"]["N"][Name("BBox")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["AP"]["N"]["BBox"].append(bDecimal(0))
        annot["AP"]["N"]["BBox"].append(bDecimal(0))
        annot["AP"]["N"]["BBox"].append(bDecimal(rectangle.width))
        annot["AP"]["N"]["BBox"].append(bDecimal(100))

        # return
        return self._append_annotation(annot)

    def append_stamp_annotation(
        self,
        rectangle: Rectangle,
        name: RubberStampAnnotationIconType = RubberStampAnnotationIconType.DRAFT,
        contents: Optional[str] = None,
        color: Optional[Color] = None,
    ) -> "Page":
        """
        A rubber stamp annotation (PDF 1.3) displays text or graphics intended to look as if they were stamped on the
        page with a rubber stamp. When opened, it shall display a pop-up window containing the text of the associated
        note. Table 181 shows the annotation dictionary entries specific to this type of annotation.
        """
        # create generic annotation
        annot = self._create_annotation(
            rectangle=rectangle, contents=contents, color=color
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Stamp for a rubber stamp annotation.
        annot[Name("Subtype")] = Name("Stamp")

        # (Optional) The name of an icon that shall be used in displaying the annotation. Conforming readers shall provide predefined icon
        # appearances for at least the following standard names:
        # Approved, Experimental, NotApproved, AsIs,
        # Expired, NotForPublicRelease, Confidential, Final, Sold,
        # Departmental, ForComment, TopSecret, Draft, ForPublicRelease
        # Additional names may be supported as well. Default value: Draft.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Name entry; see Table 168 and 12.5.5, “Appearance Streams.”
        annot[Name("Name")] = name.value

        # (Optional; PDF 1.4) The constant opacity value that shall be used in
        # painting the annotation (see Sections 11.2, “Overview of Transparency,”
        # and 11.3.7, “Shape and Opacity Computations”). This value shall apply to
        # all visible elements of the annotation in its closed state (including its
        # background and border) but not to the pop-up window that appears when
        # the annotation is opened.
        annot[Name("CA")] = bDecimal(1)

        # return
        return self._append_annotation(annot)

    def append_caret_annotation(self) -> "Page":
        """
        A caret annotation (PDF 1.5) is a visual symbol that indicates the presence of text edits. Table 180 lists the
        entries specific to caret annotations.
        """
        # TODO
        return self

    def append_ink_annotation(self) -> "Page":
        """
        An ink annotation (PDF 1.3) represents a freehand “scribble” composed of one or more disjoint paths. When
        opened, it shall display a pop-up window containing the text of the associated note. Table 182 shows the
        annotation dictionary entries specific to this type of annotation.
        """
        # TODO
        return self

    def append_popup_annotation(self) -> "Page":
        """
        A pop-up annotation (PDF 1.3) displays text in a pop-up window for entry and editing. It shall not appear alone
        but is associated with a markup annotation, its parent annotation, and shall be used for editing the parent’s text.
        It shall have no appearance stream or associated actions of its own and shall be identified by the Popup entry
        in the parent’s annotation dictionary (see Table 174). Table 183 shows the annotation dictionary entries specific
        to this type of annotation.
        """
        # TODO
        return self

    def append_file_attachment_annotation(self) -> "Page":
        """
        A file attachment annotation (PDF 1.3) contains a reference to a file, which typically shall be embedded in the
        PDF file (see 7.11.4, “Embedded File Streams”).
        """
        # TODO
        return self

    def append_sound_annotation(self) -> "Page":
        """
        A sound annotation (PDF 1.2) shall analogous to a text annotation except that instead of a text note, it contains
        sound recorded from the computer’s microphone or imported from a file. When the annotation is activated, the
        sound shall be played. The annotation shall behave like a text annotation in most ways, with a different icon (by
        default, a speaker) to indicate that it represents a sound. Table 185 shows the annotation dictionary entries
        specific to this type of annotation. Sound objects are discussed in 13.3, “Sounds.”
        """
        # TODO
        return self

    def append_movie_annotation(self) -> "Page":
        """
        A movie annotation (PDF 1.2) contains animated graphics and sound to be presented on the computer screen
        and through the speakers. When the annotation is activated, the movie shall be played. Table 186 shows the
        annotation dictionary entries specific to this type of annotation. Movies are discussed in 13.4, “Movies.”
        """
        # TODO
        return self

    def append_widget_annotation(self) -> "Page":
        """
        Interactive forms (see 12.7, “Interactive Forms”) use widget annotations (PDF 1.2) to represent the appearance
        of fields and to manage user interactions. As a convenience, when a field has only a single associated widget
        annotation, the contents of the field dictionary (12.7.3, “Field Dictionaries”) and the annotation dictionary may
        be merged into a single dictionary containing entries that pertain to both a field and an annotation.
        """
        # TODO
        return self

    def append_screen_annotation(self) -> "Page":
        """
        A screen annotation (PDF 1.5) specifies a region of a page upon which media clips may be played. It also
        serves as an object from which actions can be triggered. 12.6.4.13, “Rendition Actions” discusses the
        relationship between screen annotations and rendition actions. Table 187 shows the annotation dictionary
        entries specific to this type of annotation.
        """
        # TODO
        return self

    def append_printer_mark_annotation(self) -> "Page":
        """
        A printer’s mark annotation (PDF 1.4) represents a graphic symbol, such as a registration target, colour bar, or
        cut mark, that may be added to a page to assist production personnel in identifying components of a multiple-
        plate job and maintaining consistent output during production. See 14.11.3, “Printer’s Marks,” for further
        discussion.
        """
        # TODO
        return self

    def append_trap_net_annotation(self) -> "Page":
        """
        A trap network annotation (PDF 1.3) may be used to define the trapping characteristics for a page of a PDF
        document.
        """
        # TODO
        return self

    def append_watermark_annotation(
        self,
        rectangle: Rectangle,
        contents: str,
    ) -> "Page":
        """
        A watermark annotation (PDF 1.6) shall be used to represent graphics that shall be printed at a fixed size and
        position on a page, regardless of the dimensions of the printed page. The FixedPrint entry of a watermark
        annotation dictionary (see Table 190) shall be a dictionary that contains values for specifying the size and
        position of the annotation (see Table 191).
        """
        # TODO
        return self

    def append_3d_annotation(self) -> "Page":
        """
        3D annotations (PDF 1.6) are the means by which 3D artwork shall be represented in a PDF document.
        Table 298 shows the entries specific to a 3D annotation dictionary. Table 164 describes the entries common to
        all annotation dictionaries.

        In addition to these entries, a 3D annotation shall provide an appearance stream in its AP entry (see Table 164)
        that has a normal appearance (the N entry in Table 168). This appearance may be used by applications that do
        not support 3D annotations and by all applications for the initial display of the annotation.
        """
        # TODO
        return self

    def append_redact_annotation(
        self,
        rectangle: Rectangle,
        overlay_text: Optional[str] = None,
        repeat_overlay_text: Optional[bool] = None,
        line_width: Decimal = Decimal(1),
        stroke_color: Optional[Color] = HexColor("ff0000"),
        fill_color: Optional[Color] = None,
    ) -> "Page":
        """
        A redaction annotation (PDF 1.7) identifies content that is intended to be removed from the document. The
        intent of redaction annotations is to enable the following process:

        a) Content identification. A user applies redact annotations that specify the pieces or regions of content that
        should be removed. Up until the next step is performed, the user can see, move and redefine these
        annotations.

        b) Content removal. The user instructs the viewer application to apply the redact annotations, after which the
        content in the area specified by the redact annotations is removed. In the removed content’s place, some
        marking appears to indicate the area has been redacted. Also, the redact annotations are removed from
        the PDF document.

        Redaction annotations provide a mechanism for the first step in the redaction process (content identification).
        This allows content to be marked for redaction in a non-destructive way, thus enabling a review process for
        evaluating potential redactions prior to removing the specified content.
        """

        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle)

        # (Required) The type of annotation that this dictionary describes; shall
        # be Redact for a redaction annotation.
        annot[Name("Subtype")] = Name("Redact")

        # (Optional) An array of three numbers in the range 0.0 to 1.0
        # specifying the components, in the DeviceRGB colour space, of the
        # interior colour with which to fill the redacted region after the affected
        # content has been removed. If this entry is absent, the interior of the
        # redaction region is left transparent. This entry is ignored if the RO
        # entry is present.
        if fill_color is not None:
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(bDecimal(fill_color.to_rgb().red))
            annot["IC"].append(bDecimal(fill_color.to_rgb().green))
            annot["IC"].append(bDecimal(fill_color.to_rgb().blue))

        # (Optional) A text string specifying the overlay text that should be
        # drawn over the redacted region after the affected content has been
        # removed. This entry is ignored if the RO entry is present.
        if overlay_text is not None:
            annot[Name("OverlayText")] = String(overlay_text)

        # (Optional) If true, then the text specified by OverlayText should be
        # repeated to fill the redacted region after the affected content has been
        # removed. This entry is ignored if the RO entry is present. Default
        # value: false.
        if repeat_overlay_text is not None:
            assert overlay_text is not None
            annot[Name("Repeat")] = Boolean(repeat_overlay_text)

        # (Optional; PDF 1.2) An appearance dictionary specifying how the
        # annotation shall be presented visually on the page (see 12.5.5,
        # “Appearance Streams”). Individual annotation handlers may ignore this
        # entry and provide their own appearances.
        annot[Name("AP")] = Dictionary()
        annot["AP"][Name("N")] = Stream()
        annot["AP"]["N"][Name("Type")] = Name("XObject")
        annot["AP"]["N"][Name("Subtype")] = Name("Form")
        appearance_stream_content = "q"
        if stroke_color is not None:
            appearance_stream_content += " %f %f %f RG" % (
                stroke_color.to_rgb().red,
                stroke_color.to_rgb().green,
                stroke_color.to_rgb().blue,
            )
        if fill_color is not None:
            appearance_stream_content += " %f %f %f rg" % (
                fill_color.to_rgb().red,
                fill_color.to_rgb().green,
                fill_color.to_rgb().blue,
            )
        if stroke_color is not None and fill_color is not None:
            appearance_stream_content += " %f w 0 0 100 100 re b" % line_width
        elif stroke_color is not None:
            appearance_stream_content += " %f w 0 0 100 100 re s" % line_width
        elif fill_color is not None:
            appearance_stream_content += " %f w 0 0 100 100 re f" % line_width
        appearance_stream_content += " Q"
        annot["AP"]["N"][Name("DecodedBytes")] = bytes(
            appearance_stream_content, "latin1"
        )
        annot["AP"]["N"][Name("Bytes")] = zlib.compress(
            annot["AP"]["N"][Name("DecodedBytes")]
        )
        annot["AP"]["N"][Name("Length")] = bDecimal(
            len(annot["AP"]["N"][Name("Bytes")])
        )
        annot["AP"]["N"][Name("Filter")] = Name("FlateDecode")

        # The lower-left corner of the bounding box (BBox) is set to coordinates (0, 0) in the form coordinate system.
        # The box’s top and right coordinates are taken from the dimensions of the annotation rectangle (the Rect
        # entry in the widget annotation dictionary).
        annot["AP"]["N"][Name("BBox")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["AP"]["N"]["BBox"].append(bDecimal(0))
        annot["AP"]["N"]["BBox"].append(bDecimal(0))
        annot["AP"]["N"]["BBox"].append(bDecimal(100))
        annot["AP"]["N"]["BBox"].append(bDecimal(100))

        # return
        return self._append_annotation(annot)

    def apply_redact_annotations(
        self, rectangles_to_redact: typing.List[Rectangle] = []
    ):
        """
        This function applies the redaction annotations on this Page
        """
        from borb.pdf.canvas.redacted_canvas_stream_processor import (
            RedactedCanvasStreamProcessor,
        )

        rectangles_to_redact += [
            Rectangle(
                x["Rect"][0],
                x["Rect"][1],
                x["Rect"][2] - x["Rect"][0],
                x["Rect"][3] - x["Rect"][1],
            )
            for x in self["Annots"]
            if "Subtype" in x and x["Subtype"] == "Redact" and "Rect" in x
        ]

        # apply redaction
        redacted_canvas_content: bytes = (
            RedactedCanvasStreamProcessor(self, Canvas(), rectangles_to_redact)
            .read(io.BytesIO(self["Contents"]["DecodedBytes"]), [])
            .get_redacted_content()  # type: ignore [attr-defined]
        )

        # update Page Contents (Stream)
        self["Contents"][Name("DecodedBytes")] = redacted_canvas_content
        self["Contents"][Name("Bytes")] = zlib.compress(
            self["Contents"]["DecodedBytes"], 9
        )
        self["Contents"][Name("Length")] = bDecimal(len(self["Contents"]["Bytes"]))
