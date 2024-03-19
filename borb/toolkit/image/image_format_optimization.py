#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener resizes all Image objects on a Page
to fit their actual dimensions (ensuring they are not bigger than they need to be)
"""
import typing

from PIL import Image as PILImageModule

from borb.io.read.pdf_object import PDFObject
from borb.io.read.types import Name
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.page.page import Page


class ImageFormatOptimization(EventListener):
    """
    This implementation of EventListener resizes all Image objects on a Page
    to fit their actual dimensions (ensuring they are not bigger than they need to be)
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(ImageFormatOptimization, self).__init__()
        self._current_page: typing.Optional[Page] = None

    #
    # PRIVATE
    #

    def _event_occurred(self, event: "Event") -> None:
        if isinstance(event, BeginPageEvent):
            self._current_page = event.get_page()
        if isinstance(event, ImageRenderEvent):
            self._render_image(event)

    def _render_image(self, image_render_event: "ImageRenderEvent"):
        source_image: PILImageModule.Image = image_render_event.get_image()  # type: ignore[valid-type]

        # get desired width/height
        w0: int = int(image_render_event.get_width())  # type: ignore [attr-defined]
        h0: int = int(image_render_event.get_height())  # type: ignore [attr-defined]

        # get current width/height
        w1: int = source_image.width  # type: ignore[attr-defined]
        h1: int = source_image.height  # type: ignore[attr-defined]

        # get image resource name
        assert self._current_page is not None
        resource_name: typing.Optional[Name] = next(
            iter(
                [
                    k
                    for k, v in self._current_page["Resources"]["XObject"].items()
                    if id(v) == id(source_image)
                ]
            ),
            None,
        )
        assert resource_name is not None

        # resize
        if (w0 * h0) < (w1 * h1):
            resized_image: PILImageModule.Image = source_image.resize((w0, h0))  # type: ignore[attr-defined, valid-type]
            PDFObject.add_pdf_object_methods(resized_image)
            self._current_page["Resources"]["XObject"][resource_name] = resized_image
            resized_image.set_parent(self._current_page["Resources"]["XObject"][resource_name])  # type: ignore[attr-defined]

    #
    # PUBLIC
    #
