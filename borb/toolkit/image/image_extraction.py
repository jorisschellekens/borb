#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener extracts all Image objects on a Page
"""
import io
import typing

from PIL import Image as PILImageModule

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class ImageExtraction(EventListener):
    """
    This implementation of EventListener extracts all Image objects on a Page
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Constructs a new SimpleImageExtraction
        """
        self._image_render_info_per_page = {}
        self._current_page: int = -1

    #
    # PRIVATE
    #

    def _begin_page(self, page: Page):
        self._current_page += 1

    def _event_occurred(self, event: "Event") -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, ImageRenderEvent):
            self._render_image(event)

    def _render_image(self, image_render_event: "ImageRenderEvent"):
        # init if needed
        if self._current_page not in self._image_render_info_per_page:
            self._image_render_info_per_page[self._current_page] = []

        # append ImageRenderEvent
        self._image_render_info_per_page[self._current_page].append(
            image_render_event.get_image()
        )

    #
    # PUBLIC
    #

    def get_images(self) -> typing.Dict[int, typing.List[PILImageModule.Image]]:
        """
        This function returns a typing.List[Image] on a given page
        """
        return self._image_render_info_per_page

    @staticmethod
    def get_images_from_pdf(
        pdf: Document,
    ) -> typing.Dict[int, typing.List[PILImageModule.Image]]:
        """
        This function returns the images used in a given PDF
        :param pdf:     the PDF to be analysed
        :return:        the images (typing.List[PIL.Image.Image]) in the PDF
        """
        images_of_each_page: typing.Dict[int, typing.List[PILImageModule.Image]] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])

            # register EventListener
            cse: "ImageExtraction" = ImageExtraction()

            # process Page
            cse._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [cse])
            cse._event_occurred(EndPageEvent(page))

            # set in page
            images_of_each_page[page_nr] = cse.get_images()[0]

        # return
        return images_of_each_page
