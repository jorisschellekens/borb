#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A text annotation represents a “sticky note” attached to a point in the PDF document. When closed, the
annotation shall appear as an icon; when open, it shall display a pop-up window containing the text of the note
in a font and size chosen by the conforming reader. Text annotations shall not scale and rotate with the page;
they shall behave as if the NoZoom and NoRotate annotation flags (see Table 165) were always set. Table 172
shows the annotation dictionary entries specific to this type of annotation.
"""
import enum
import typing

from borb.io.read.types import Boolean
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.annotation import Annotation


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


class TextAnnotation(Annotation):
    """
    A text annotation represents a “sticky note” attached to a point in the PDF document. When closed, the
    annotation shall appear as an icon; when open, it shall display a pop-up window containing the text of the note
    in a font and size chosen by the conforming reader. Text annotations shall not scale and rotate with the page;
    they shall behave as if the NoZoom and NoRotate annotation flags (see Table 165) were always set. Table 172
    shows the annotation dictionary entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        bounding_box: Rectangle,
        contents: str,
        color: typing.Optional[Color] = None,
        open: typing.Optional[bool] = None,
        text_annotation_icon: TextAnnotationIconType = TextAnnotationIconType.COMMENT,
    ):
        super(TextAnnotation, self).__init__(
            bounding_box=bounding_box, contents=contents, color=color
        )

        # specific for text annotations
        self[Name("Subtype")] = Name("Text")

        # (Optional) A flag specifying whether the annotation shall initially be
        # displayed open. Default value: false (closed).
        if open is not None:
            self[Name("Open")] = Boolean(open)

        # (Optional) The name of an icon that shall be used in displaying the
        # annotation. Conforming readers shall provide predefined icon
        # appearances for at least the following standard names:
        # Comment, Key, Note, Help, NewParagraph, Paragraph, Insert
        # Additional names may be supported as well. Default value: Note.
        # The annotation dictionary’s AP entry, if present, shall take precedence
        # over the Name entry; see Table 168 and 12.5.5, “Appearance Streams.”
        self[Name("Name")] = text_annotation_icon.value

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #
