#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener extracts all text from a PDF Document
"""
import typing
from decimal import Decimal
from functools import cmp_to_key

from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import (
    ChunkOfTextRenderEvent,
    LeftToRightComparator,
)
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import Event, EventListener
from borb.pdf.page.page import Page


class SimpleTextExtraction(EventListener):
    """
    This implementation of EventListener extracts all text from a PDF Document
    """

    def __init__(self):
        self._text_render_info_per_page: typing.Dict[
            int, typing.List[ChunkOfTextRenderEvent]
        ] = {}
        self._text_per_page: typing.Dict[int, str] = {}
        self._current_page: int = -1

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, ChunkOfTextRenderEvent):
            self._render_text(event)
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, EndPageEvent):
            self._end_page(event.get_page())

    def get_text_for_page(self, page_nr: int) -> str:
        """
        This function returns all text on a given page
        """
        return self._text_per_page[page_nr] if page_nr in self._text_per_page else ""

    def _render_text(self, text_render_info: ChunkOfTextRenderEvent):

        # init if needed
        if self._current_page not in self._text_render_info_per_page:
            self._text_render_info_per_page[self._current_page] = []

        # append TextRenderInfo
        self._text_render_info_per_page[self._current_page].append(text_render_info)

    def _begin_page(self, page: Page):
        self._current_page += 1

    def _end_page(self, page: Page):

        # get TextRenderInfo objects on page
        tris = (
            self._text_render_info_per_page[self._current_page]
            if self._current_page in self._text_render_info_per_page
            else []
        )

        # remove no-op
        tris = [x for x in tris if x._text is not None]
        tris = [x for x in tris if len(x._text.replace(" ", "")) != 0]

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
                text += t._text
                last_baseline_right = t.get_baseline().x + t.get_baseline().width
                last_baseline_bottom = t.get_baseline().y
                continue

            # check text
            if t._text.startswith(" ") or text.endswith(" "):
                text += t._text
                last_baseline_right = t.get_baseline().x + t.get_baseline().width
                continue

            # add space if needed
            delta = abs(last_baseline_right - t.get_baseline().x)
            space_width = round(t.get_space_character_width_estimate_in_user_space(), 1)
            text += " " if (space_width * Decimal(0.90) < delta) else ""

            # normal append
            text += t._text
            last_baseline_right = t.get_baseline().x + t.get_baseline().width
            continue

        # store text
        self._text_per_page[self._current_page] = text
