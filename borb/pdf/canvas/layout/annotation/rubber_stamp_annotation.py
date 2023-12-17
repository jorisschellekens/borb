#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A rubber stamp annotation (PDF 1.3) displays text or graphics intended to look as if they were stamped on the
page with a rubber stamp. When opened, it shall display a pop-up window containing the text of the associated
note. Table 181 shows the annotation dictionary entries specific to this type of annotation.
"""
import enum
import typing

from borb.io.read.types import Decimal as bDecimal
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


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


class RubberStampAnnotation(Annotation):
    """
    A rubber stamp annotation (PDF 1.3) displays text or graphics intended to look as if they were stamped on the
    page with a rubber stamp. When opened, it shall display a pop-up window containing the text of the associated
    note. Table 181 shows the annotation dictionary entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        bounding_box: Rectangle,
        color: typing.Optional[Color] = None,
        contents: typing.Optional[str] = None,
        name: RubberStampAnnotationIconType = RubberStampAnnotationIconType.DRAFT,
    ):
        super(RubberStampAnnotation, self).__init__(
            bounding_box=bounding_box, contents=contents, color=color
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Stamp for a rubber stamp annotation.
        self[Name("Subtype")] = Name("Stamp")

        # (Optional) The name of an icon that shall be used in displaying the annotation. Conforming readers shall provide predefined icon
        # appearances for at least the following standard names:
        # Approved, Experimental, NotApproved, AsIs,
        # Expired, NotForPublicRelease, Confidential, Final, Sold,
        # Departmental, ForComment, TopSecret, Draft, ForPublicRelease
        # Additional names may be supported as well. Default value: Draft.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Name entry; see Table 168 and 12.5.5, “Appearance Streams.”
        self[Name("Name")] = name.value

        # (Optional; PDF 1.4) The constant opacity value that shall be used in
        # painting the annotation (see Sections 11.2, “Overview of Transparency,”
        # and 11.3.7, “Shape and Opacity Computations”). This value shall apply to
        # all visible elements of the annotation in its closed state (including its
        # background and border) but not to the pop-up window that appears when
        # the annotation is opened.
        self[Name("CA")] = bDecimal(1)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
