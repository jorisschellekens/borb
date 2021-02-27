#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class represents a single page in a PDF document
"""
import datetime
import typing
from decimal import Decimal
from typing import Optional, Tuple

from ptext.io.read.types import Decimal as pDecimal
from ptext.io.read.types import Dictionary, Name, List, String, Boolean
from ptext.pdf.canvas.color.color import Color, X11Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page_info import PageInfo


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
        self["MediaBox"].append(pDecimal(0))
        self["MediaBox"].append(pDecimal(0))
        self["MediaBox"].append(pDecimal(width))
        self["MediaBox"].append(pDecimal(height))

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
        annot["Rect"].append(pDecimal(rectangle.get_x()))
        annot["Rect"].append(pDecimal(rectangle.get_y()))
        annot["Rect"].append(pDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["Rect"].append(pDecimal(rectangle.get_y() + rectangle.get_height()))

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
        annot[Name("F")] = pDecimal(4)

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
            annot["Border"].append(pDecimal(border_horizontal_corner_radius))
            annot["Border"].append(pDecimal(border_vertical_corner_radius))
            annot["Border"].append(pDecimal(border_width))

        # (Optional; PDF 1.1) An array of numbers in the range 0.0 to 1.0,
        # representing a colour used for the following purposes:
        # The background of the annotation’s icon when closed
        # The title bar of the annotation’s pop-up window
        # The border of a link annotation
        # The number of array elements determines the colour space in which the
        # colour shall be defined
        if color is not None:
            color_max = pDecimal(256)
            annot[Name("C")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["C"].append(pDecimal(color.to_rgb().red / color_max))
            annot["C"].append(pDecimal(color.to_rgb().green / color_max))
            annot["C"].append(pDecimal(color.to_rgb().blue / color_max))

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
        timestamp_str += "+00"
        return timestamp_str

    def append_text_annotation(
        self,
        rectangle: Rectangle,
        contents: str,
        open: Optional[bool] = None,
        color: Optional[Color] = None,
        name_of_icon: Optional[str] = None,
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

        if open is not None:
            annot[Name("Open")] = Boolean(open)

        if name_of_icon is not None:
            assert name_of_icon in [
                "Comment",
                "Key",
                "Note",
                "Help",
                "NewParagraph",
                "Paragraph",
                "Insert",
            ]
            annot[Name("Name")] = Name(name_of_icon)

        # annot[Name("State")] = None
        # annot[Name("StateModel")] = None

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

    def append_link_annotation(
        self,
        rectangle: Rectangle,
        page: Decimal,
        destination_type: str,
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
        assert destination_type in [
            "XYZ",
            "Fit",
            "FitH",
            "FitV",
            "FitR",
            "FitB",
            "FitBH",
            "FitBV",
        ]
        destination = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        destination.append(pDecimal(page))
        destination.append(Name(destination_type))
        if destination_type == "XYZ":
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is not None
                and zoom is not None
            )
            destination.append(pDecimal(left))
            destination.append(pDecimal(top))
            destination.append(pDecimal(zoom))
        if destination_type == "Fit":
            assert (
                left is None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
        if destination_type == "FitH":
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(pDecimal(top))
        if destination_type == "FitV":
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(pDecimal(left))
        if destination_type == "FitR":
            assert (
                left is not None
                and bottom is not None
                and right is not None
                and top is not None
                and zoom is None
            )
            destination.append(pDecimal(left))
            destination.append(pDecimal(bottom))
            destination.append(pDecimal(right))
            destination.append(pDecimal(top))
        if destination_type == "FitBH":
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(pDecimal(top))
        if destination_type == "FitBV":
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(pDecimal(left))
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

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

    def append_free_text_annotation(self) -> "Page":
        """
        A free text annotation (PDF 1.3) displays text directly on the page. Unlike an ordinary text annotation (see
        12.5.6.4, “Text Annotations”), a free text annotation has no open or closed state; instead of being displayed in a
        pop-up window, the text shall be always visible. Table 174 shows the annotation dictionary entries specific to
        this type of annotation. 12.7.3.3, “Variable Text” describes the process of using these entries to generate the
        appearance of the text in these annotations.
        """

        # TODO
        return self

    def append_line_annotation(
        self,
        start_point: Tuple[Decimal, Decimal],
        end_point: Tuple[Decimal, Decimal],
        left_line_end_style: Optional[str] = None,
        right_line_end_style: Optional[str] = None,
        stroke_color: Color = X11Color("Black"),
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
        if left_line_end_style is not None:
            assert left_line_end_style in [
                "Square",
                "Circle",
                "Diamond",
                "OpenArrow",
                "ClosedArrow",
                "None",
                "Butt",
                "ROpenArrow",
                "RClosedArrow",
                "Slash",
            ]
            annot["LE"].append(Name(left_line_end_style))
        else:
            annot["LE"].append(Name("None"))
        if right_line_end_style is not None:
            assert right_line_end_style in [
                "Square",
                "Circle",
                "Diamond",
                "OpenArrow",
                "ClosedArrow",
                "None",
                "Butt",
                "ROpenArrow",
                "RClosedArrow",
                "Slash",
            ]
            annot["LE"].append(Name(right_line_end_style))
        else:
            annot["LE"].append(Name("None"))

        # (Optional; PDF 1.4) An array of numbers that shall be in the range 0.0 to
        # 1.0 and shall specify the interior color with which to fill the annotation’s
        # rectangle or ellipse. The number of array elements determines the colour
        # space in which the colour shall be defined
        if stroke_color is not None:
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(stroke_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(stroke_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(stroke_color.to_rgb().blue / color_max))

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

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
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(fill_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().blue / color_max))

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
            annot["RD"].append(pDecimal(rectangle_difference[0]))
            annot["RD"].append(pDecimal(rectangle_difference[1]))
            annot["RD"].append(pDecimal(rectangle_difference[2]))
            annot["RD"].append(pDecimal(rectangle_difference[3]))

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

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
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(fill_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().blue / color_max))

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
            annot["RD"].append(pDecimal(rectangle_difference[0]))
            annot["RD"].append(pDecimal(rectangle_difference[1]))
            annot["RD"].append(pDecimal(rectangle_difference[2]))
            annot["RD"].append(pDecimal(rectangle_difference[3]))

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

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

        annot[Name("Subtype")] = Name("Polygon")

        annot[Name("CA")] = pDecimal(1)

        annot[Name("Vertices")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        for p in points:
            annot["Vertices"].append(pDecimal(p[0]))
            annot["Vertices"].append(pDecimal(p[1]))

        # (Optional; PDF 1.4) An array of two names specifying the line ending
        # styles that shall be used in drawing the line. The first and second
        # elements of the array shall specify the line ending styles for the endpoints
        # defined, respectively, by the first and second pairs of coordinates, (x 1 , y 1 )
        # and (x 2 , y 2 ), in the L array. Table 176 shows the possible values. Default
        # value: [ /None /None ].
        annot[Name("LE")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["LE"].append(Name("None"))
        annot["LE"].append(Name("None"))

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

    def append_polyline_annotation(
        self,
        points: typing.List[Tuple[Decimal, Decimal]],
        stroke_color: Color,
        left_line_end_style: Optional[str] = None,
        right_line_end_style: Optional[str] = None,
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

        annot[Name("Subtype")] = Name("PolyLine")

        annot[Name("CA")] = pDecimal(1)

        annot[Name("Vertices")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        for p in points:
            annot["Vertices"].append(pDecimal(p[0]))
            annot["Vertices"].append(pDecimal(p[1]))

        # (Optional; PDF 1.4) An array of two names specifying the line ending
        # styles that shall be used in drawing the line. The first and second
        # elements of the array shall specify the line ending styles for the endpoints
        # defined, respectively, by the first and second pairs of coordinates, (x 1 , y 1 )
        # and (x 2 , y 2 ), in the L array. Table 176 shows the possible values. Default
        # value: [ /None /None ].
        annot[Name("LE")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        if left_line_end_style is not None:
            assert left_line_end_style in [
                "Square",
                "Circle",
                "Diamond",
                "OpenArrow",
                "ClosedArrow",
                "None",
                "Butt",
                "ROpenArrow",
                "RClosedArrow",
                "Slash",
            ]
            annot["LE"].append(Name(left_line_end_style))
        else:
            annot["LE"].append(Name("None"))
        if right_line_end_style is not None:
            assert right_line_end_style in [
                "Square",
                "Circle",
                "Diamond",
                "OpenArrow",
                "ClosedArrow",
                "None",
                "Butt",
                "ROpenArrow",
                "RClosedArrow",
                "Slash",
            ]
            annot["LE"].append(Name(right_line_end_style))
        else:
            annot["LE"].append(Name("None"))

        if fill_color is not None:
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(fill_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().blue / color_max))

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

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
        annot["QuadPoints"].append(pDecimal(rectangle.get_x()))
        annot["QuadPoints"].append(pDecimal(rectangle.get_y()))
        # x4, y4
        annot["QuadPoints"].append(pDecimal(rectangle.get_x()))
        annot["QuadPoints"].append(pDecimal(rectangle.get_y() + rectangle.get_height()))
        # x2, y2
        annot["QuadPoints"].append(pDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["QuadPoints"].append(pDecimal(rectangle.get_y()))
        # x3, y3
        annot["QuadPoints"].append(pDecimal(rectangle.get_x() + rectangle.get_width()))
        annot["QuadPoints"].append(pDecimal(rectangle.get_y() + rectangle.get_height()))

        # border
        annot[Name("Border")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
        annot["Border"].append(pDecimal(0))
        annot["Border"].append(pDecimal(0))
        annot["Border"].append(pDecimal(1))

        # CA
        annot[Name("CA")] = pDecimal(1)

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

    def append_underline_annotation(
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
        # TODO
        return self

    def append_squiggly_annotation(self) -> "Page":
        """
        Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
        underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
        the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
        annotations.
        """
        # TODO
        return self

    def append_strike_out_annotation(self) -> "Page":
        """
        Text markup annotations shall appear as highlights, underlines, strikeouts (all PDF 1.3), or jagged (“squiggly”)
        underlines (PDF 1.4) in the text of a document. When opened, they shall display a pop-up window containing
        the text of the associated note. Table 179 shows the annotation dictionary entries specific to these types of
        annotations.
        """
        # TODO
        return self

    def append_stamp_annotation(
        self,
        name: str,
        rectangle: Rectangle,
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

        # specific for text annotations
        annot[Name("Subtype")] = Name("Stamp")

        if name is not None:
            assert name in [
                "Approved",
                "Experimental",
                "NotApproved",
                "Asis",
                "Expired",
                "NotForPublicRelease",
                "Confidential",
                "Final",
                "Sold",
                "Departmental",
                "ForComment",
                "TopSecret",
                "Draft",
                "ForPublicRelease",
            ]
            annot[Name("Name")] = Name(name)

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

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
        return self

    def append_redact_annotation(
        self,
        rectangle: Rectangle,
        overlay_text: Optional[str] = None,
        repeat_overlay_text: Optional[bool] = None,
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
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(fill_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(fill_color.to_rgb().blue / color_max))

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

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

    def apply_redact_annotations(self):
        pass
