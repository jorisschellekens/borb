#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content that appears below a specified image on the PDF page.

This filter is used to identify and process elements, typically text, that are positioned
beneath a designated image within the content stream. By setting an image as a
reference point, `BelowImage` enables selective extraction, manipulation, or analysis
of content that appears below that image, making it useful for document processing tasks
that depend on spatial relationships between images and surrounding text.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.end_page_event import EndPageEvent
from borb.pdf.toolkit.source.event.image_event import ImageEvent
from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
from borb.pdf.toolkit.source.event.text_event import TextEvent


class BelowImage(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content that appears below a specified image on the PDF page.

    This filter is used to identify and process elements, typically text, that are positioned
    beneath a designated image within the content stream. By setting an image as a
    reference point, `BelowImage` enables selective extraction, manipulation, or analysis
    of content that appears below that image, making it useful for document processing tasks
    that depend on spatial relationships between images and surrounding text.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the BelowImage filter.

        This constructor sets up the necessary structures for processing events related
        to content located below images. It prepares the filter to capture events as the
        PDF content streams are processed, allowing for filtering based on the position
        of content relative to images.
        """
        super().__init__()
        self.__events_per_page: typing.Dict[int, typing.List[Event]] = {}  # type: ignore[annotation-unchecked]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        self.__events_per_page[event.get_page_nr()] = self.__events_per_page.get(
            event.get_page_nr(), []
        ) + [event]

        # IF there is no next Pipe
        # THEN return
        next_pipe: typing.Optional[Pipe] = self.get_next()
        if next_pipe is None:
            return

        # EndPageEvent
        if isinstance(event, EndPageEvent):
            y_limit: float = min(
                [
                    x.get_y()
                    for x in self.__events_per_page[event.get_page_nr()]
                    if isinstance(x, ImageEvent)
                ]
                + [event.get_page().get_size()[1]]
            )

            for event_in_page in self.__events_per_page[event.get_page_nr()]:
                # pass along to the next Pipe
                if (
                    isinstance(event_in_page, ShapeFillEvent)
                    or isinstance(event_in_page, ShapeStrokeEvent)
                    or isinstance(event_in_page, ImageEvent)
                    or isinstance(event_in_page, TextEvent)
                ):
                    if event_in_page.get_y() <= y_limit:
                        next_pipe.process(event_in_page)
                else:
                    next_pipe.process(event_in_page)
