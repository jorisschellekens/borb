#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A free text annotation (PDF 1.3) displays text directly on the page. Unlike an ordinary text annotation (see
12.5.6.4, “Text Annotations”), a free text annotation has no open or closed state; instead of being displayed in a
pop-up window, the text shall be always visible. Table 174 shows the annotation dictionary entries specific to
this type of annotation. 12.7.3.3, “Variable Text” describes the process of using these entries to generate the
appearance of the text in these annotations.
"""
import typing
from decimal import Decimal

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


class FreeTextAnnotation(Annotation):
    """
    A free text annotation (PDF 1.3) displays text directly on the page. Unlike an ordinary text annotation (see
    12.5.6.4, “Text Annotations”), a free text annotation has no open or closed state; instead of being displayed in a
    pop-up window, the text shall be always visible. Table 174 shows the annotation dictionary entries specific to
    this type of annotation. 12.7.3.3, “Variable Text” describes the process of using these entries to generate the
    appearance of the text in these annotations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        bounding_box: Rectangle,
        contents: str,
        background_color: typing.Optional[Color] = None,
        font: Font = StandardType1Font("Helvetica"),
        font_color: Color = HexColor("000000"),
        font_size: Decimal = Decimal(12),
    ):
        super(FreeTextAnnotation, self).__init__(
            bounding_box=bounding_box, contents=contents, color=background_color
        )
        self._font: Font = font
        self._font_color_rgb: "RGBColor" = font_color.to_rgb()  # type: ignore [name-defined]
        self._font_size: Decimal = font_size
        self._font_name: str = "F0"

        # specific for text annotations
        self[Name("Subtype")] = Name("FreeText")

        # (Optional; PDF 1.1) A set of flags specifying various characteristics of
        # the annotation (see 12.5.3, “Annotation Flags”). Default value: 0.
        self[Name("F")] = bDecimal(20)

        # (Required) The default appearance string that shall be used in formatting
        # the text (see 12.7.3.3, “Variable Text”).
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the DA entry; see Table 168 and 12.5.5, “Appearance Streams.”
        self[Name("DA")] = String(
            "/%s %f Tf %f %f %f rg"
            % (
                self._font_name,
                self._font_size,
                self._font_color_rgb.red,
                self._font_color_rgb.green,
                self._font_color_rgb.blue,
            )
        )

        # (Optional; PDF 1.4) A code specifying the form of quadding (justification)
        # that shall be used in displaying the annotation’s text:
        # 0 Left-justified
        # 1 Centered
        # 2 Right-justified
        # Default value: 0 (left-justified).
        self[Name("Q")] = bDecimal(0)

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
        self[Name("IT")] = Name("FreeTextTypeWriter")

    #
    # PRIVATE
    #

    def _embed_font_in_page(self, page: "Page") -> None:  # type: ignore[name-defined]
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary()
        if "Font" not in page["Resources"]:
            page["Resources"][Name("Font")] = Dictionary()
        font_number: int = len(page["Resources"]["Font"])
        font_name: str = "F%d" % font_number
        while font_name in page["Resources"]["Font"]:
            font_number += 1
            font_name = "F%d" % font_number
        page["Resources"]["Font"][Name(font_name)] = self._font

        # (Required) The default appearance string that shall be used in formatting
        # the text (see 12.7.3.3, “Variable Text”).
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the DA entry; see Table 168 and 12.5.5, “Appearance Streams.”
        self[Name("DA")] = String(
            "/%s %f Tf %f %f %f rg"
            % (
                self._font_name,
                self._font_size,
                self._font_color_rgb.red,
                self._font_color_rgb.green,
                self._font_color_rgb.blue,
            )
        )

    #
    # PUBLIC
    #
