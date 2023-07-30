#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts all paragraphs of text from a PDF Document
"""
import io
import typing
from decimal import Decimal

from borb.datastructure.disjoint_set import disjointset
from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.text.simple_line_of_text_extraction import SimpleLineOfTextExtraction


class SimpleParagraphExtraction(SimpleLineOfTextExtraction):
    """
    This implementation of EventListener extracts all paragraphs of text from a PDF Document
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        minimum_horizontal_overlap_percentage: Decimal = Decimal(0.80),
        maximum_multiplied_leading: Decimal = Decimal(1.40),
    ):
        super(SimpleParagraphExtraction, self).__init__()
        self._minimum_horizontal_overlap_percentage = (
            minimum_horizontal_overlap_percentage
        )
        self._maximum_multiplied_leading = maximum_multiplied_leading
        self._paragraphs_per_page: typing.Dict[int, typing.List[Paragraph]] = {}

    #
    # PRIVATE
    #

    def _end_page(self, page: Page):
        super(SimpleParagraphExtraction, self)._end_page(page)

        # build initial disjointset
        line_of_text_disjoint_set = disjointset()
        for line_of_text in self._lines_of_text_per_page[self._current_page_number]:
            line_of_text_disjoint_set.add(line_of_text)

        # merge all LineOfText objects that represent a line of text
        for l0 in line_of_text_disjoint_set:
            for l1 in line_of_text_disjoint_set:
                if l0 == l1:
                    continue
                if line_of_text_disjoint_set.find(l0) == line_of_text_disjoint_set.find(
                    l1
                ):
                    continue

                if (
                    l0.get_previous_layout_box().get_width() == 0
                    or l1.get_previous_layout_box().get_width() == 0
                ):
                    continue

                # determine overlap
                overlap_percentage = self._overlap(
                    l0.get_previous_layout_box(), l1.get_previous_layout_box()
                ) / min(
                    l0.get_previous_layout_box().width,
                    l1.get_previous_layout_box().width,
                )

                # determine leading
                leading = abs(
                    l0.get_previous_layout_box().y - l1.get_previous_layout_box().y
                ) / min(
                    l0.get_previous_layout_box().height,
                    l1.get_previous_layout_box().height,
                )

                if (
                    overlap_percentage >= self._minimum_horizontal_overlap_percentage
                    and leading <= self._maximum_multiplied_leading
                ):
                    line_of_text_disjoint_set.union(l0, l1)
                    break

        # combine partitions into Paragraph objects
        paragraphs: typing.List[Paragraph] = []
        for line_of_text_partition in line_of_text_disjoint_set.sets():
            lines_of_text = [x for x in line_of_text_partition]

            # determine text
            txt = "".join([x.get_text() + "\n" for x in lines_of_text])[:-1]

            # create / append paragraph
            p: LayoutElement = Paragraph(
                text=txt,
                font=lines_of_text[0].get_font(),
                font_color=lines_of_text[0].get_font_color(),
                font_size=lines_of_text[0].get_font_size(),
            )
            p._previous_layout_box = Rectangle(
                min([l.get_previous_layout_box().x for l in lines_of_text]),
                min([l.get_previous_layout_box().y for l in lines_of_text]),
                max(
                    [
                        l.get_previous_layout_box().x
                        + l.get_previous_layout_box().width
                        for l in lines_of_text
                    ]
                )
                - min([l.get_previous_layout_box().x for l in lines_of_text]),
                max(
                    [
                        l.get_previous_layout_box().y
                        + l.get_previous_layout_box().height
                        for l in lines_of_text
                    ]
                )
                - min([l.get_previous_layout_box().y for l in lines_of_text]),
            )
            assert isinstance(p, Paragraph)
            paragraphs.append(p)

        # add to dict
        self._paragraphs_per_page[self._current_page_number] = paragraphs

    def _overlap(self, r0: Rectangle, r1: Rectangle) -> Decimal:
        # rectangles do not overlap (r0 is on the left side)
        if max(r0.x, r0.x + r0.width) < min(r1.x, r1.x + r1.width):
            return Decimal(0)
        # rectangles do not overlap (r1 is on the left side)
        if max(r1.x, r1.x + r1.width) < min(r0.x, r0.x + r0.width):
            return Decimal(0)
        a = max(min(r0.x, r0.x + r0.width), min(r1.x, r1.x + r1.width))
        b = min(max(r0.x, r0.x + r0.width), max(r1.x, r1.x + r1.width))
        return abs(a - b)

    #
    # PUBLIC
    #

    def get_paragraphs(self) -> typing.Dict[int, typing.List[Paragraph]]:
        """
        This function returns the paragraphs on a given PDF
        """
        return self._paragraphs_per_page

    @staticmethod
    def get_paragraphs_from_pdf(
        pdf: Document,
    ) -> typing.Dict[int, typing.List[Paragraph]]:
        """
        This function returns the Paragraph objects for a given PDF (per page)
        :param pdf:     the PDF to be analyzed
        :return:        the Paragraph objects per page (represented by typing.Dict[int, typing.List[Paragraph]])
        """
        paragraphs_per_page: typing.Dict[int, typing.List[Paragraph]] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])
            # register EventListener
            l: "SimpleParagraphExtraction" = SimpleParagraphExtraction()
            # process Page
            l._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [l])
            l._event_occurred(EndPageEvent(page))
            # add to output dictionary
            paragraphs_per_page[page_nr] = l.get_paragraphs()[0]
        # return
        return paragraphs_per_page
