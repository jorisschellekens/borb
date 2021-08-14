# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener enables you to
    extract font-related information from a Document
"""
import typing
from typing import List

from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.event_listener import Event, EventListener
from borb.pdf.canvas.font.font import Font


class FontExtraction(EventListener):
    """
    This implementation of EventListener enables you to
    extract font-related information from a Document
    """

    def __init__(self):
        self._fonts_per_page: typing.Dict[int, typing.List[Font]] = {}
        self._current_page: int = -1

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event)

    def _begin_page(self, event: BeginPageEvent):

        # update page number
        self._current_page += 1
        self._fonts_per_page[self._current_page] = []

        # get page
        page = event.get_page()
        if page is None:
            return

        # get resources
        if "Resources" not in page or not isinstance(page["Resources"], dict):
            return
        if "Font" not in page["Resources"] or not isinstance(
            page["Resources"]["Font"], dict
        ):
            return

        for _, f in page["Resources"]["Font"].items():
            self._fonts_per_page[self._current_page].append(f)

    def get_fonts_for_page(self, page_number: int) -> List[Font]:
        """
        This function returns all fonts used on a given page
        """
        return (
            self._fonts_per_page[page_number]
            if page_number in self._fonts_per_page
            else []
        )

    def get_font_names_for_page(self, page_number: int) -> List[str]:
        """
        This function returns all font names used on a given page
        """
        out: typing.List[str] = []
        for x in self.get_fonts_for_page(page_number):
            font_name: typing.Optional[str] = x.get_font_name()
            if font_name is not None:
                out.append(font_name)
        return out
