#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class converts a PDF to MarkDown
"""
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.page.page import Page


class PDFToMarkDown(EventListener):
    """
    This class converts a PDF to MarkDown
    """

    def __init__(self):
        self.current_page = -1
        self.markdown_per_page = {}

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        # TODO

    def _begin_page(self, page: Page):
        self.current_page += 1
        self.markdown_per_page[self.current_page] = ""

    def get_markdown_per_page(self, page_number: int) -> str:
        """
        This function returns the markdown content (as a string) for a given page
        """
        return (
            self.markdown_per_page[page_number]
            if page_number in self.markdown_per_page
            else ""
        )
