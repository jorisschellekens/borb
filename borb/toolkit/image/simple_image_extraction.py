#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener extracts all Image objects on a Page
"""
from typing import List

from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.event_listener import Event, EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.page.page import Page
from PIL import Image  # type: ignore [import]


class SimpleImageExtraction(EventListener):
    """
    This implementation of EventListener extracts all Image objects on a Page
    """

    def __init__(self):
        """
        Constructs a new SimpleImageExtraction
        """
        self._image_render_info_per_page = {}
        self._current_page: int = -1

    def _event_occurred(self, event: "Event") -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, ImageRenderEvent):
            self._render_image(event)

    def get_images_for_page(self, page_nr: int) -> List[Image.Image]:
        """
        This function returns a typing.List[Image] on a given page
        """
        return (
            self._image_render_info_per_page[page_nr]
            if page_nr in self._image_render_info_per_page
            else []
        )

    def _render_image(self, image_render_event: "ImageRenderEvent"):

        # init if needed
        if self._current_page not in self._image_render_info_per_page:
            self._image_render_info_per_page[self._current_page] = []

        # append ImageRenderEvent
        self._image_render_info_per_page[self._current_page].append(
            image_render_event.get_image()
        )

    def _begin_page(self, page: Page):
        self._current_page += 1
