#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a rubber stamp annotation, which displays text or graphics resembling a stamped image.

A rubber stamp annotation (PDF 1.3) visually simulates the appearance of being stamped on the
page with a rubber stamp. When opened, it displays a pop-up window containing the text of the
associated note.

Table 181 shows the annotation dictionary entries specific to this type of annotation.
"""
import enum
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.primitives import name


class RubberStampAnnotation(Annotation):
    """
    Represents a rubber stamp annotation, which displays text or graphics resembling a stamped image.

    A rubber stamp annotation (PDF 1.3) visually simulates the appearance of being stamped on the
    page with a rubber stamp. When opened, it displays a pop-up window containing the text of the
    associated note.

    Table 181 shows the annotation dictionary entries specific to this type of annotation.
    """

    class RubberStampAnnotationType(enum.Enum):
        """
        Defines the names of icons used to display rubber stamp annotations.

        This enumeration specifies the predefined icon appearances for rubber stamp annotations.
        Conforming readers must provide support for at least the following standard names:

        - Approved
        - Experimental
        - NotApproved
        - AsIs
        - Expired
        - Sold
        - Departmental
        - NotForPublicRelease
        - Confidential
        - Final
        - ForComment
        - TopSecret
        - Draft
        - ForPublicRelease

        Additional names may also be supported. The default value is "Draft".

        If present, the annotation dictionary’s AP entry takes precedence over the Name entry;
        refer to Table 168 and section 12.5.5, “Appearance Streams,” for further details.
        """

        APPROVED = 2
        AS_IS = 3
        CONFIDENTIAL = 5
        DEPARTMENTAL = 7
        DRAFT = 11
        EXPERIMENTAL = 13
        EXPIRED = 17
        FINAL = 19
        FOR_COMMENT = 23
        FOR_PUBLIC_RELEASE = 29
        NOT_APPROVED = 31
        NOT_FOR_PUBLIC_RELEASE = 37
        SOLD = 43
        TOP_SECRET = 47

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
        rubber_stamp_annotation_type: RubberStampAnnotationType = RubberStampAnnotationType.DRAFT,
        size: typing.Tuple[int, int] = (100, 100),
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new `RubberStampAnnotation` object for rendering a stamp annotation in a PDF.

        This constructor allows customization of various layout and style properties for
        the stamp annotation, such as background color, borders, size, contents, and alignment.
        These properties define the appearance and positioning of the annotation within the PDF page.

        :param background_color:           Optional background color for the stamp annotation.
        :param border_color:               Optional border color for the annotation container.
        :param border_dash_pattern:        Dash pattern used for the annotation border lines.
        :param border_dash_phase:          Phase offset for the dash pattern in the annotation borders.
        :param border_width_bottom:        Width of the bottom border of the annotation container.
        :param border_width_left:          Width of the left border of the annotation container.
        :param border_width_right:         Width of the right border of the annotation container.
        :param border_width_top:           Width of the top border of the annotation container.
        :param contents:                   Optional text content of the stamp annotation.
        :param horizontal_alignment:       Horizontal alignment of the annotation (default is LEFT).
        :param padding_bottom:             Padding inside the annotation container at the bottom.
        :param padding_left:               Padding inside the annotation container on the left side.
        :param padding_right:              Padding inside the annotation container on the right side.
        :param padding_top:                Padding inside the annotation container at the top.
        :param rubber_stamp_annotation_type: Type of rubber stamp annotation (default is DRAFT).
        :param size:                       Tuple representing the width and height of the annotation.
        :param vertical_alignment:         Vertical alignment of the annotation (default is TOP).
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
            fill_color=None,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            stroke_color=None,
            size=size,
            vertical_alignment=vertical_alignment,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Stamp for a rubber stamp annotation.
        self["Subtype"] = name("Stamp")

        # (Optional) The name of an icon that shall be used in displaying the
        # annotation. Conforming readers shall provide predefined icon
        # appearances for at least the following standard names:
        # Approved, Experimental, NotApproved, AsIs, Expired,
        # Sold, Departmental, NotForPublicRelease, Confidential, Final,
        # ForComment, TopSecret, Draft, ForPublicRelease
        # Additional names may be supported as well. Default value: Draft.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Name entry; see Table 168 and 12.5.5, “Appearance Streams.”
        # fmt: off
        self["Name"] = {
            RubberStampAnnotation.RubberStampAnnotationType.APPROVED: name("Approved"),
            RubberStampAnnotation.RubberStampAnnotationType.EXPERIMENTAL: name("Experimental"),
            RubberStampAnnotation.RubberStampAnnotationType.NOT_APPROVED: name("NotApproved"),
            RubberStampAnnotation.RubberStampAnnotationType.AS_IS: name("AsIs"),
            RubberStampAnnotation.RubberStampAnnotationType.EXPIRED: name("Expired"),
            RubberStampAnnotation.RubberStampAnnotationType.SOLD: name("Sold"),
            RubberStampAnnotation.RubberStampAnnotationType.DEPARTMENTAL: name("Departmental"),
            RubberStampAnnotation.RubberStampAnnotationType.NOT_FOR_PUBLIC_RELEASE: name("NotForPublicRelease"),
            RubberStampAnnotation.RubberStampAnnotationType.CONFIDENTIAL: name("Confidential"),
            RubberStampAnnotation.RubberStampAnnotationType.FINAL: name("Final"),
            RubberStampAnnotation.RubberStampAnnotationType.FOR_COMMENT: name("ForComment"),
            RubberStampAnnotation.RubberStampAnnotationType.TOP_SECRET: name("TopSecret"),
            RubberStampAnnotation.RubberStampAnnotationType.DRAFT: name("Draft"),
            RubberStampAnnotation.RubberStampAnnotationType.FOR_PUBLIC_RELEASE: name("ForPublicRelease"),
        }[rubber_stamp_annotation_type]
        # fmt: on

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
