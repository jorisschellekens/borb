#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener enables you to
    extract font-related information from a Document
"""
import typing

from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.font.font import Font


class FontExtraction(EventListener):
    """
    This implementation of EventListener enables you to
    extract font-related information from a Document
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        self._fonts_per_page: typing.Dict[int, typing.List[Font]] = {}
        self._current_page: int = -1

    #
    # PRIVATE
    #

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

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event)

    #
    # PUBLIC
    #

    def get_font_names(self) -> typing.Dict[int, typing.List[str]]:
        """
        This function returns all font names used in the PDF
        """
        out: typing.Dict[int, typing.List[str]] = {}
        for k, v in self._fonts_per_page.items():
            if k not in out:
                out[k] = []
            for i in v:
                font_name: typing.Optional[str] = i.get_font_name()
                if font_name is not None:
                    out[k].append(font_name)
        return out

    def get_fonts(self) -> typing.Dict[int, typing.List[Font]]:
        """
        This function returns all fonts used on a given PDF
        """
        return self._fonts_per_page
