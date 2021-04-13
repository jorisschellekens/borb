#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts all text from a PDF Document
"""
from decimal import Decimal
from functools import cmp_to_key

from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.chunk_of_text_render_event import (
    ChunkOfTextRenderEvent,
    LeftToRightComparator,
)
from ptext.pdf.canvas.event.end_page_event import EndPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.page.page import Page


class SimpleTextExtraction(EventListener):
    """
    This implementation of EventListener extracts all text from a PDF Document
    """

    def __init__(self):
        self.text_render_info_per_page = {}
        self.text_per_page = {}
        self.current_page = -1

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, ChunkOfTextRenderEvent):
            self._render_text(event)
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, EndPageEvent):
            self._end_page(event.get_page())

    def get_text(self, page_nr: int) -> str:
        """
        This function returns all text on a given page
        """
        return self.text_per_page[page_nr] if page_nr in self.text_per_page else ""

    def _render_text(self, text_render_info: ChunkOfTextRenderEvent):

        # init if needed
        if self.current_page not in self.text_render_info_per_page:
            self.text_render_info_per_page[self.current_page] = []

        # append TextRenderInfo
        self.text_render_info_per_page[self.current_page].append(text_render_info)

    def _begin_page(self, page: Page):
        self.current_page += 1

    def _end_page(self, page: Page):

        # get TextRenderInfo objects on page
        tris = (
            self.text_render_info_per_page[self.current_page]
            if self.current_page in self.text_render_info_per_page
            else []
        )

        # remove no-op
        tris = [x for x in tris if x.text is not None]
        tris = [x for x in tris if len(x.text.replace(" ", "")) != 0]

        # skip empty
        if len(tris) == 0:
            return

        # sort according to comparator
        sorted(tris, key=cmp_to_key(LeftToRightComparator.cmp))

        # iterate over the TextRenderInfo objects to get the text
        last_baseline_bottom = tris[0].get_baseline().y
        last_baseline_right = tris[0].get_baseline().x
        text = ""
        for t in tris:

            # add newline if needed
            if abs(t.get_baseline().y - last_baseline_bottom) > 10 and len(text) > 0:
                if text.endswith(" "):
                    text = text[0:-1]
                text += "\n"
                text += t.text
                last_baseline_right = t.get_baseline().x + t.get_baseline().width
                last_baseline_bottom = t.get_baseline().y
                continue

            # check text
            if t.text.startswith(" ") or text.endswith(" "):
                text += t.text
                last_baseline_right = t.get_baseline().x + t.get_baseline().width
                continue

            # add space if needed
            delta = abs(last_baseline_right - t.get_baseline().x)
            space_width = round(t.get_space_character_width_estimate(), 1)
            text += " " if (space_width * Decimal(0.90) < delta) else ""

            # normal append
            text += t.text
            last_baseline_right = t.get_baseline().x + t.get_baseline().width
            continue

        # store text
        self.text_per_page[self.current_page] = text
