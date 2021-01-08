import datetime
from decimal import Decimal
from typing import Optional, Tuple

from ptext.io.read_transform.types import Decimal as pDecimal
from ptext.io.read_transform.types import Dictionary, Name, List, String, Boolean
from ptext.pdf.canvas.color.color import Color, RGBColor
from ptext.pdf.page.page_info import PageInfo


class Page(Dictionary):
    def get_page_info(self) -> PageInfo:
        return PageInfo(self)

    def get_document(self) -> "Document":  # type: ignore [name-defined]
        return self.get_root()  # type: ignore [attr-defined]

    #
    # ANNOTATIONS
    #

    def _create_annotation(
        self,
        rectangle: Tuple[Decimal, Decimal, Decimal, Decimal],
        contents: Optional[str] = None,
        color: Optional[Color] = None,
        border_horizontal_corner_radius: Optional[Decimal] = None,
        border_vertical_corner_radius: Optional[Decimal] = None,
        border_width: Optional[Decimal] = None,
    ):
        # TODO : page 383 PDF32000.book.pdf
        annot = Dictionary()

        # (Optional) The type of PDF object that this dictionary describes; if
        # present, shall be Annot for an annotation dictionary.
        annot[Name("Type")] = Name("Annot")

        # (Required) The annotation rectangle, defining the location of the
        # annotation on the page in default user space units.
        annot[Name("Rect")] = List().set_can_be_referenced(False)
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
            annot[Name("Border")] = List().set_can_be_referenced(False)
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
            annot[Name("C")] = List().set_can_be_referenced(False)
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
        destination = List().set_can_be_referenced(False)
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
        return self

    def append_line_annotation(self) -> "Page":
        return self

    def append_square_annotation(self) -> "Page":
        return self

    def append_circle_annotation(self) -> "Page":
        return self

    def append_polygon_annotation(self) -> "Page":
        return self

    def append_polyline_annotation(self) -> "Page":
        return self

    def append_highlight_annotation(self) -> "Page":
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
        name: Optional[str] = None,
    ) -> "Page":
        # create generic annotation
        annot = self._create_annotation(rectangle=rectangle)

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

    def append_redact_annotation(self) -> "Page":
        return self
