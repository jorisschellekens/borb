import datetime
from decimal import Decimal
from typing import Optional, Tuple

from ptext.io.read_transform.types import Decimal as pDecimal
from ptext.io.read_transform.types import Dictionary, Name, List, String, Boolean
from ptext.pdf.canvas.color.color import Color
from ptext.pdf.page.page_info import PageInfo


class Page(Dictionary):
    def __init__(self):
        super(Page, self).__init__()

        # size: A4 portrait
        self[Name("MediaBox")] = List().set_can_be_referenced(False)
        self["MediaBox"].append(pDecimal(0))
        self["MediaBox"].append(pDecimal(0))
        self["MediaBox"].append(pDecimal(595))
        self["MediaBox"].append(pDecimal(842))

    def get_page_info(self) -> PageInfo:
        return PageInfo(self)

    def get_document(self) -> "Document":  # type: ignore [name-defined]
        return self.get_root()  # type: ignore [attr-defined]

    #
    # ANNOTATIONS
    #

    def get_annotations(self) -> List:
        if "Annots" not in self:
            self[Name("Annots")] = List()
        return self["Annots"]

    def _create_annotation(
        self,
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
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
        annot["Rect"].append(pDecimal(rectangle[0]))
        annot["Rect"].append(pDecimal(rectangle[1]))
        annot["Rect"].append(pDecimal(rectangle[2]))
        annot["Rect"].append(pDecimal(rectangle[3]))

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
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
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
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        page: Decimal,
        location_on_page: str,
        left: Optional[Decimal] = None,
        bottom: Optional[Decimal] = None,
        right: Optional[Decimal] = None,
        top: Optional[Decimal] = None,
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
        assert location_on_page in [
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
        destination.append(Name(location_on_page))
        if location_on_page == "XYZ":
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
        if location_on_page == "Fit":
            assert (
                left is None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
        if location_on_page == "FitH":
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(pDecimal(top))
        if location_on_page == "FitV":
            assert (
                left is not None
                and bottom is None
                and right is None
                and top is None
                and zoom is None
            )
            destination.append(pDecimal(left))
        if location_on_page == "FitR":
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
        if location_on_page == "FitBH":
            assert (
                left is None
                and bottom is None
                and right is None
                and top is not None
                and zoom is None
            )
            destination.append(pDecimal(top))
        if location_on_page == "FitBV":
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

    def append_line_annotation(self) -> "Page":
        """
        The purpose of a line annotation (PDF 1.3) is to display a single straight line on the page. When opened, it shall
        display a pop-up window containing the text of the associated note. Table 175 shows the annotation dictionary
        entries specific to this type of annotation.
        """
        # TODO
        return self

    def append_square_annotation(
        self,
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        color: Color,
        interior_color: Optional[Color] = None,
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
        annot = self._create_annotation(rectangle=rectangle, color=color)

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
        if interior_color is not None:
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(interior_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(interior_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(interior_color.to_rgb().blue / color_max))

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
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        color: Color,
        rectangle_difference: Optional[
            Tuple[Decimal, Decimal, Decimal, Decimal]
        ] = None,
        interior_color: Optional[Color] = None,
    ) -> "Page":
        """
        Square and circle annotations (PDF 1.3) shall display, respectively, a rectangle or an ellipse on the page. When
        opened, they shall display a pop-up window containing the text of the associated note. The rectangle or ellipse
        shall be inscribed within the annotation rectangle defined by the annotation dictionary’s Rect entry (see
        Table 168).
        """

        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle, color=color)

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
        if interior_color is not None:
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(interior_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(interior_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(interior_color.to_rgb().blue / color_max))

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

    def append_polygon_annotation(self) -> "Page":
        # TODO
        return self

    def append_polyline_annotation(self) -> "Page":
        # TODO
        return self

    def append_highlight_annotation(
        self,
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        color: Color,
    ) -> "Page":
        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle, color=color)
        annot.pop("Rect")

        # (Required) The type of annotation that this dictionary describes; shall
        # be Highlight, Underline, Squiggly, or StrikeOut for a highlight,
        # underline, squiggly-underline, or strikeout annotation, respectively.
        annot[Name("Subtype")] = Name("Highlight")

        # (Required) An array of 8 × n numbers specifying the coordinates of n
        # quadrilaterals in default user space. Each quadrilateral shall
        # encompasses a word or group of contiguous words in the text
        # underlying the annotation. The coordinates for each quadrilateral shall
        # be given in the order
        # x 1 y 1 x 2 y 2 x 3 y 3 x 4 y 4
        annot[Name("QuadPoints")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]

        return self

    def append_underline_annotation(self) -> "Page":
        return self

    def append_squiggly_annotation(self) -> "Page":
        return self

    def append_strike_out_annotation(self) -> "Page":
        return self

    def append_stamp_annotation(
        self,
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        contents: Optional[str] = None,
        color: Optional[Color] = None,
        name: Optional[str] = None,
    ) -> "Page":
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
        return self

    def append_ink_annotation(self) -> "Page":
        return self

    def append_popup_annotation(self) -> "Page":
        return self

    def append_file_attachment_annotation(self) -> "Page":
        return self

    def append_sound_annotation(self) -> "Page":
        return self

    def append_movie_annotation(self) -> "Page":
        return self

    def append_widget_annotation(self) -> "Page":
        return self

    def append_screen_annotation(self) -> "Page":
        return self

    def append_printer_mark_annotation(self) -> "Page":
        return self

    def append_trap_net_annotation(self) -> "Page":
        return self

    def append_watermark_annotation(
        self,
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        contents: str,
    ) -> "Page":
        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle, contents=contents)

        # specific for text annotations
        annot[Name("Subtype")] = Name("Watermark")

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annot)

        # return
        return self

    def append_3d_annotation(self) -> "Page":
        return self

    def append_redact_annotation(
        self,
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        overlay_text: Optional[str] = None,
        repeat_overlay_text: Optional[bool] = None,
        interior_color: Optional[Color] = None,
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
        if interior_color is not None:
            color_max = pDecimal(256)
            annot[Name("IC")] = List().set_can_be_referenced(False)  # type: ignore [attr-defined]
            annot["IC"].append(pDecimal(interior_color.to_rgb().red / color_max))
            annot["IC"].append(pDecimal(interior_color.to_rgb().green / color_max))
            annot["IC"].append(pDecimal(interior_color.to_rgb().blue / color_max))

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
