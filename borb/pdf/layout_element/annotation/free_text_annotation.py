#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a free text annotation in a PDF document.

A free text annotation (PDF 1.3) displays text directly on the page. Unlike an ordinary text
annotation (see 12.5.6.4, “Text Annotations”), a free text annotation does not have an open or
closed state; instead, the text is always visible.

Table 174 shows the annotation dictionary entries specific to this type of annotation.
Section 12.7.3.3, “Variable Text,” describes the process of using these entries to generate
the appearance of the text in these annotations.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.font.font import Font
from borb.pdf.font.simple_font.standard_14_fonts import Standard14Fonts
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import name


class FreeTextAnnotation(Annotation):
    """
    Represents a free text annotation in a PDF document.

    A free text annotation (PDF 1.3) displays text directly on the page. Unlike an ordinary text
    annotation (see 12.5.6.4, “Text Annotations”), a free text annotation does not have an open or
    closed state; instead, the text is always visible.

    Table 174 shows the annotation dictionary entries specific to this type of annotation.
    Section 12.7.3.3, “Variable Text,” describes the process of using these entries to generate
    the appearance of the text in these annotations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        contents: str,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        font_color: Color = X11Color.BLACK,
        font_size: int = 12,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: typing.Tuple[int, int] = (100, 100),
        stroke_color: typing.Optional[Color] = X11Color.WHITE,
        text_alignment: LayoutElement.TextAlignment = LayoutElement.TextAlignment.LEFT,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a FreeTextAnnotation, a customizable text annotation in a PDF.

        Initialize a FreeTextAnnotation object, which allows for creating a customizable annotation containing free text
        within a PDF document.

        :param contents:                The text content of the annotation.
        :param background_color:        The background color of the annotation. Defaults to None (transparent).
        :param border_color:            The color of the annotation's border. Defaults to None.
        :param border_dash_pattern:     A list specifying the dash pattern for the annotation's border. Defaults to an empty list (solid border).
        :param border_dash_phase:       The phase offset for the border dash pattern. Defaults to 0.
        :param border_width_bottom:     The width of the bottom border of the annotation. Defaults to 0.
        :param border_width_left:       The width of the left border of the annotation. Defaults to 0.
        :param border_width_right:      The width of the right border of the annotation. Defaults to 0.
        :param border_width_top:        The width of the top border of the annotation. Defaults to 0.
        :param font_color:              The color of the text font. Defaults to X11Color.BLACK.
        :param font_size:               The size of the text font in points. Defaults to 12.
        :param horizontal_alignment:    The horizontal alignment of the annotation within its bounding box (e.g., left, center, right). Defaults to LEFT.
        :param margin_bottom:           The bottom margin within the annotation. Defaults to 0.
        :param margin_left:             The left margin within the annotation. Defaults to 0.
        :param margin_right:            The right margin within the annotation. Defaults to 0.
        :param margin_top:              The top margin within the annotation. Defaults to 0.
        :param padding_bottom:          The bottom padding inside the annotation, between the text and the border. Defaults to 0.
        :param padding_left:            The left padding inside the annotation. Defaults to 0.
        :param padding_right:           The right padding inside the annotation. Defaults to 0.
        :param padding_top:             The top padding inside the annotation. Defaults to 0.
        :param size:                    A tuple specifying the width and height of the annotation. Defaults to (100, 100).
        :param stroke_color:            The stroke color applied to the text. Defaults to X11Color.WHITE.
        :param text_alignment:          The alignment of the text within the annotation (e.g., left, center, right). Defaults to LEFT.
        :param vertical_alignment:      The vertical alignment of the annotation within its bounding box (e.g., top, middle, bottom). Defaults to TOP.
        """
        assert font_size >= 0, "The font_size must be a non-negative value."
        self.__font_color: Color = font_color
        self.__font_size: int = font_size
        self.__text_alignment: LayoutElement.TextAlignment = text_alignment
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            contents=contents,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            size=size,
            stroke_color=stroke_color,
            vertical_alignment=vertical_alignment,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # FreeText for a free text annotation.
        self["Subtype"] = name("FreeText")

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
        # EXAMPLE
        # A Border value of [ 0 0 1 [ 3 2 ] ] specifies a border 1
        # unit wide, with square corners, drawn with 3-unit
        # dashes alternating with 2-unit gaps.
        # NOTE
        # (PDF 1.2) The dictionaries for some annotation types (such
        # as free text and polygon annotations) can include the BS
        # entry. That entry specifies a border style dictionary that has
        # more settings than the array specified for the Border entry.
        # If an annotation dictionary includes the BS entry, then the
        # Border entry is ignored.
        # Default value: [ 0 0 1 ].
        self[name("Border")] = [0, 0, 0]

        # (Optional; PDF 1.1) A set of flags specifying various characteristics of
        # the annotation (see 12.5.3, “Annotation Flags”). Default value: 0.
        self["F"] = 20

        # (Required) The default appearance string that shall be used in formatting
        # the text (see 12.7.3.3, “Variable Text”).
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the DA entry; see Table 168 and 12.5.5, “Appearance Streams.”
        font_color_rgb: RGBColor = self.__font_color.to_rgb_color()
        self["DA"] = "/%s %f Tf %f %f %f rg" % (
            "/F1",
            font_size,
            font_color_rgb.get_red() / 255,
            font_color_rgb.get_green() / 255,
            font_color_rgb.get_blue() / 255,
        )

        # (Optional; PDF 1.4) A code specifying the form of quadding (justification)
        # that shall be used in displaying the annotation’s text:
        # 0 Left-justified
        # 1 Centered
        # 2 Right-justified
        # Default value: 0 (left-justified).
        self["Q"] = 0
        if self.__text_alignment == LayoutElement.TextAlignment.LEFT:
            self["Q"] = 0
        elif self.__text_alignment == LayoutElement.TextAlignment.CENTERED:
            self["Q"] = 1
        elif self.__text_alignment == LayoutElement.TextAlignment.RIGHT:
            self["Q"] = 2

        # (Optional; PDF 1.6) A name describing the intent of the free text
        # annotation (see also the IT entry in Table 170). The following values shall
        # be valid:
        # - FreeText:           The annotation is intended to function as a plain
        #                       free-text annotation. A plain free-text annotation
        #                       is also known as a text box comment.
        #
        # - FreeTextCallout:    The annotation is intended to function as a
        #                       callout. The callout is associated with an area on
        #                       the page through the callout line specified in CL.
        #
        # - FreeTextTypeWriter: The annotation is intended to function as a click-
        #                       to-type or typewriter object and no callout line is
        #                       drawn.
        # Default value: FreeText
        self["IT"] = name("FreeText")

    #
    # PRIVATE
    #

    def __get_font_resource_name(self, font: Font, page: Page):
        # create resources if needed
        if "Resources" not in page:
            page[name("Resources")] = {}
        if "Font" not in page["Resources"]:
            page["Resources"][name("Font")] = {}

        # IF the font is already present
        # THEN return that particular font
        # fmt: off
        font_resource_name = [k for k, v in page["Resources"]["Font"].items() if v == font]
        if len(font_resource_name) > 0:
            return font_resource_name[0]
        # fmt: on

        # IF the font is not yet present
        # THEN create it
        font_index = len(page["Resources"]["Font"]) + 1
        page["Resources"]["Font"][name("F%d" % font_index)] = font
        return name("F%d" % font_index)

    #
    # PUBLIC
    #

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        # handle font
        # fmt: off
        font_name: str = self.__get_font_resource_name(font=Standard14Fonts.get("Helvetica"), page=page) # type: ignore[arg-type]
        # fmt: on

        # (Required) The default appearance string that shall be used in formatting
        # the text (see 12.7.3.3, “Variable Text”).
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the DA entry; see Table 168 and 12.5.5, “Appearance Streams.”
        font_color_rgb: RGBColor = self.__font_color.to_rgb_color()
        self["DA"] = "/%s %f Tf %f %f %f rg" % (
            f"/{font_name}",
            self.__font_size,
            font_color_rgb.get_red() / 255,
            font_color_rgb.get_green() / 255,
            font_color_rgb.get_blue() / 255,
        )

        # call to super
        super().paint(available_space=available_space, page=page)
