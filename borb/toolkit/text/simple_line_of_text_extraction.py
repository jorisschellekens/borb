#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts all lines of text from a PDF Document
"""
import io
import typing
from decimal import Decimal
import functools

from borb.datastructure.disjoint_set import disjointset
from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import LeftToRightComparator
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.canvas.layout.text.line_of_text import LineOfText
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class SimpleLineOfTextExtraction(EventListener):
    """
    This implementation of EventListener extracts all lines of text from a PDF Document
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._chunks_of_text: typing.List[ChunkOfTextRenderEvent] = []
        self._current_page_number: int = -1
        self._current_page: typing.Optional[Page] = None
        self._lines_of_text_per_page: typing.Dict[int, typing.List[LineOfText]] = {}

    #
    # PRIVATE
    #

    def _end_page(self, page: Page):
        # build initial disjointset
        chunks_of_text_disjoint_set = disjointset()
        for x in self._chunks_of_text:
            chunks_of_text_disjoint_set.add(x)

        # merge all ChunkOfText objects that represent a line of text
        for c0 in chunks_of_text_disjoint_set:
            for c1 in chunks_of_text_disjoint_set:
                if c0 == c1:
                    continue
                r0 = c0.get_baseline()
                r1 = c1.get_baseline()
                if r0.y != r1.y:
                    continue
                gap = max(r1.x - (r0.x + r0.width), r0.x - (r1.x + r1.width))
                space_gap = (
                    c0.get_space_character_width_estimate_in_user_space()
                    if r0.x < r1.x
                    else c1.get_space_character_width_estimate_in_user_space()
                )
                if gap < space_gap * Decimal(2):
                    chunks_of_text_disjoint_set.union(c0, c1)

        # combine partitions into LineOfText objects
        lines_of_text: typing.List[LineOfText] = []
        for chunks_of_text_partition in chunks_of_text_disjoint_set.sets():
            # sort
            chunks_of_text: typing.List[ChunkOfTextRenderEvent] = [
                x for x in chunks_of_text_partition
            ]
            chunks_of_text = sorted(
                chunks_of_text, key=functools.cmp_to_key(LeftToRightComparator.cmp)
            )

            # determine text
            txt = ""
            for i, c in enumerate(chunks_of_text):
                if i == 0:
                    txt += c.get_text()
                    continue
                # decide whether we need to insert space or not
                gap = c.get_baseline().get_x() - (
                    chunks_of_text[i - 1].get_baseline().get_x()
                    + chunks_of_text[i - 1].get_baseline().get_width()
                )
                space_gap = chunks_of_text[
                    i - 1
                ].get_space_character_width_estimate_in_user_space()
                if gap > space_gap:
                    txt += " "
                txt += c.get_text()

            # build LineOfText
            l: LayoutElement = LineOfText(
                text=txt,
                font=chunks_of_text[0].get_font(),
                font_size=chunks_of_text[0].get_font_size(),
                font_color=chunks_of_text[0].get_font_color(),
            )
            l._previous_layout_box = Rectangle(
                chunks_of_text[0].get_baseline().get_x(),
                chunks_of_text[0].get_baseline().get_y(),
                chunks_of_text[-1].get_baseline().get_x()
                + chunks_of_text[-1].get_baseline().get_width()
                - chunks_of_text[0].get_baseline().get_x(),
                chunks_of_text[0].get_baseline().get_height(),
            )
            assert isinstance(l, LineOfText)
            lines_of_text.append(l)

        # add to dict
        self._lines_of_text_per_page[self._current_page_number] = lines_of_text

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, ChunkOfTextRenderEvent):
            self._chunks_of_text.append(event)
        if isinstance(event, BeginPageEvent):
            self._current_page = event.get_page()
            self._current_page_number += 1
            self._chunks_of_text = []
        if isinstance(event, EndPageEvent):
            self._end_page(event.get_page())

    #
    # PUBLIC
    #

    def get_lines_of_text(self) -> typing.Dict[int, typing.List[LineOfText]]:
        """
        This function returns the lines of text on a given PDF
        """
        return self._lines_of_text_per_page

    @staticmethod
    def get_lines_of_text_from_pdf(
        pdf: Document,
    ) -> typing.Dict[int, typing.List[LineOfText]]:
        """
        This function returns the LineOfText objects for a given PDF (per page)
        :param pdf:     the PDF to be analyzed
        :return:        the LineOfText objects per page (represented by typing.Dict[int, typing.List[LineOfText]])
        """
        lines_of_text_per_page: typing.Dict[int, typing.List[LineOfText]] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])
            # register EventListener
            l: "SimpleLineOfTextExtraction" = SimpleLineOfTextExtraction()
            # process Page
            l._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [l])
            l._event_occurred(EndPageEvent(page))
            # add to output dictionary
            lines_of_text_per_page[page_nr] = l.get_lines_of_text()[0]
        # return
        return lines_of_text_per_page
