#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a text annotation, often referred to as a "sticky note" in the PDF document.

When closed, the annotation appears as an icon; when opened, it displays a pop-up window containing the
text of the note. The font and size of the text are determined by the conforming reader.

Text annotations do not scale or rotate with the page; they behave as if the NoZoom and NoRotate
annotation flags (see Table 165) are always set.

Table 172 shows the annotation dictionary entries specific to this type of annotation.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.primitives import name


class TextAnnotation(Annotation):
    """
    Represents a text annotation, often referred to as a "sticky note" in the PDF document.

    When closed, the annotation appears as an icon; when opened, it displays a pop-up window containing the
    text of the note. The font and size of the text are determined by the conforming reader.

    Text annotations do not scale or rotate with the page; they behave as if the NoZoom and NoRotate
    annotation flags (see Table 165) are always set.

    Table 172 shows the annotation dictionary entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        contents: typing.Optional[str] = None,
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
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a TextAnnotation object to represent a text annotation in a PDF document.

        This constructor allows for customization of appearance, layout, and content for the text
        annotation, including background color, border style, alignment, margins, padding, and size.

        :param background_color: Optional; background color of the annotation.
        :param border_color: Optional; color of the annotation's border.
        :param border_dash_pattern: Dash pattern for the border as a list of integers.
        :param border_dash_phase: Starting point for the dash pattern along the border.
        :param border_width_bottom: Bottom border width.
        :param border_width_left: Left border width.
        :param border_width_right: Right border width.
        :param border_width_top: Top border width.
        :param contents: Optional; text content displayed within the annotation.
        :param horizontal_alignment: Alignment of content within the annotation horizontally.
        :param margin_bottom: Bottom margin for spacing around the annotation.
        :param margin_left: Left margin for spacing around the annotation.
        :param margin_right: Right margin for spacing around the annotation.
        :param margin_top: Top margin for spacing around the annotation.
        :param padding_bottom: Bottom padding within the annotation.
        :param padding_left: Left padding within the annotation.
        :param padding_right: Right padding within the annotation.
        :param padding_top: Top padding within the annotation.
        :param size: Tuple specifying width and height of the annotation.
        :param vertical_alignment: Alignment of content within the annotation vertically.
        """
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
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            size=size,
            vertical_alignment=vertical_alignment,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Text for a text annotation.
        self[name("Subtype")] = name("Text")

        # (Optional) A flag specifying whether the annotation shall initially be
        # displayed open. Default value: false (closed).
        self[name("Open")] = True

        # (Optional) The name of an icon that shall be used in displaying the
        # annotation. Conforming readers shall provide predefined icon
        # appearances for at least the following standard names:
        # Comment, Key, Note, Help, NewParagraph, Paragraph, Insert
        # Additional names may be supported as well. Default value: Note.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Name entry; see Table 168 and 12.5.5, “Appearance Streams.”
        self[name("Name")] = name("Note")

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
