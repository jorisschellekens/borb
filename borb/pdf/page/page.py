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
from borb.pdf.canvas.layout.annotation.annotation import Annotation
from borb.pdf.page.page_info import PageInfo


class Page(Dictionary):
    """
    This class represents a single page in a PDF document
    """

    def __init__(self, width: Decimal = Decimal(595), height: Decimal = Decimal(842)):
        super(Page, self).__init__()

        # type
        self[Name("Type")] = Name("Page")

        # size: A4 portrait
        self[Name("MediaBox")] = List().set_is_inline(True)  # type: ignore [attr-defined]
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

    def append_annotation(self, annotation: Annotation) -> "Page":
        """
        This function appends an Annotation to this Page, returning self.
        :param annotation:  the Annotation object to append to this Page
        :return:            self
        """

        # (Optional; PDF 1.4) The annotation name, a text string uniquely
        # identifying it among all the annotations on its page.
        len_annots = len(self["Annots"]) if "Annots" in self else 0
        annotation[Name("NM")] = String("annotation-{0:03d}".format(len_annots))

        # (Optional except as noted below; PDF 1.3; not used in FDF files) An
        # indirect reference to the page object with which this annotation is
        # associated.
        # This entry shall be present in screen annotations associated with
        # rendition actions (PDF 1.5; see 12.5.6.18, “Screen Annotations” and
        # 12.6.4.13, “Rendition Actions”).
        annotation[Name("P")] = self

        # append to /Annots
        if "Annots" not in self:
            self[Name("Annots")] = List()
            self["Annots"].set_parent(self)
        assert isinstance(self["Annots"], List)
        self["Annots"].append(annotation)

        # FreeTextAnnotation needs to embed resources in the Page
        if "Subtype" in annotation and annotation["Subtype"] == "FreeText":
            annotation._embed_font_in_page(self)

        # return
        return self

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
