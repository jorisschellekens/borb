#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This class implements a (single word) find/replace functionality for PDF documents.
This class uses RegularExpressionTextExtraction to find the text,
RedactAnnotation to remove the text, and Paragraph to re-insert replacement text.
"""

import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.annotation.redact_annotation import RedactAnnotation
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class SimpleFindReplace:
    """
    This class implements a (single word) find/replace functionality for PDF documents.
    This class uses RegularExpressionTextExtraction to find the text,
    RedactAnnotation to remove the text, and Paragraph to re-insert replacement text.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @staticmethod
    def sub(
        pattern: str,
        repl: str,
        doc: Document,
        page_range: typing.Optional[typing.List[int]] = None,
        repl_font: Font = StandardType1Font("Helvetica"),
        repl_font_color: typing.Optional[Color] = None,
        repl_font_horizontal_alignment: Alignment = Alignment.CENTERED,
        repl_font_size: typing.Optional[Decimal] = None,
    ) -> Document:
        """
        This function finds and replaces a regular expression in a PDF by a given piece of text
        :param pattern:                         the regular expression to be replaced
        :param repl:                            the replacement string
        :param doc:                             the PDF Document
        :param page_range:                      the pages on which to apply find/replace (if empty, this will default to all pages)
        :param repl_font:                       the Font to be used to insert the replacement text
        :param repl_font_color:                 the font_color to be used to isnert the replacement text (if empty, this will default to the original font_color)
        :param repl_font_size:                  the font_size to be used to insert the replacement text (if empty, this will default to the original font_size)
        :param repl_font_horizontal_alignment   the horizontal_alignment of the replacement text (defaults to Alignment.CENTERED)
        :return:                                the PDF Document
        """
        from borb.toolkit import RegularExpressionTextExtraction, PDFMatch

        number_of_pages: int = int(
            doc.get_document_info().get_number_of_pages() or Decimal(0)
        )
        matches_per_page: typing.Dict[
            int, typing.List[PDFMatch]
        ] = RegularExpressionTextExtraction.get_matches_for_pdf(pattern, doc)
        if page_range is None:
            page_range = [x for x in range(0, number_of_pages)]
        else:
            page_range = [x for x in page_range if x >= 0 and x < number_of_pages]
        for page_nr in page_range:
            # insert redaction annotations
            page: Page = doc.get_page(page_nr)
            for pdf_match in matches_per_page[page_nr]:
                for bounding_box in pdf_match.get_bounding_boxes():
                    page.add_annotation(RedactAnnotation(bounding_box.grow(Decimal(1))))

            # store original redact annotations
            # TODO

            # apply redact annotations
            page.apply_redact_annotations()

            # restore original redact annotations
            # TODO

            # insert new text (helvetica)
            for pdf_match in matches_per_page[page_nr]:
                # bounding box
                # fmt: off
                bb_x: Decimal = pdf_match.get_bounding_boxes()[0].get_x()
                bb_y: Decimal = pdf_match.get_bounding_boxes()[0].get_y()
                bb_h: Decimal = max([x.get_height() for x in pdf_match.get_bounding_boxes() if x.get_y() == bb_y])
                bb_w: Decimal = sum([x.get_width() for x in pdf_match.get_bounding_boxes() if x.get_y() == bb_y]) + Decimal(2)
                # fmt: on

                # determine font_size
                if repl_font_size is None:
                    repl_font_size = pdf_match.get_font_size()

                # determine font_color
                if repl_font_color is None:
                    repl_font_color = pdf_match.get_font_color()

                # put Paragraph
                if repl != "":
                    Paragraph(
                        repl,
                        font=repl_font,
                        font_size=repl_font_size,
                        font_color=repl_font_color,
                        horizontal_alignment=repl_font_horizontal_alignment,
                    ).paint(
                        page,
                        Rectangle(
                            bb_x - Decimal(0.5),
                            bb_y - Decimal(0.5),
                            bb_w + Decimal(1),
                            bb_h + Decimal(1),
                        ),
                    )

        # return
        return doc
