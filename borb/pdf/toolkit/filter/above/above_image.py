#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams to selectively retain content that appears above image elements on the page.

`AboveImage` extends `PageContentStreamFilter` to provide specialized filtering within a
PDF page's content stream, isolating content that appears visually above image objects.
This can be useful for various document processing tasks, such as extracting or modifying
text or vector graphics that are positioned above images on the page.

This class is typically used in contexts where content segregation based on image position
is required, such as in PDF content analysis, layered content extraction, or visual structure
modifications in a PDF.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.end_page_event import EndPageEvent
from borb.pdf.toolkit.source.event.image_event import ImageEvent
from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
from borb.pdf.toolkit.source.event.text_event import TextEvent


class AboveImage(Pipe):
    """
    A filter class for processing PDF page content streams to selectively retain content that appears above image elements on the page.

    `AboveImage` extends `PageContentStreamFilter` to provide specialized filtering within a
    PDF page's content stream, isolating content that appears visually above image objects.
    This can be useful for various document processing tasks, such as extracting or modifying
    text or vector graphics that are positioned above images on the page.

    This class is typically used in contexts where content segregation based on image position
    is required, such as in PDF content analysis, layered content extraction, or visual structure
    modifications in a PDF.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize the AboveImage filter.

        This constructor sets up the necessary structures for processing events related
        to content located above images. It prepares the filter to capture events as the
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
                    x.get_y() + x.get_height()
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
                    if event_in_page.get_y() >= y_limit:
                        next_pipe.process(event_in_page)
                else:
                    next_pipe.process(event_in_page)
