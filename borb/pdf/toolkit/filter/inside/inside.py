#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content that appears within a specified rectangular region on the PDF page.

The `Inside` filter identifies and processes elements located within a defined area, allowing
for selective extraction or manipulation of text, images, or graphics within that region. This
filter is useful for isolating content within specific boundaries, such as tables, headers,
footers, or highlighted sections.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe


class Inside(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content that appears within a specified rectangular region on the PDF page.

    The `Inside` filter identifies and processes elements located within a defined area, allowing
    for selective extraction or manipulation of text, images, or graphics within that region. This
    filter is useful for isolating content within specific boundaries, such as tables, headers,
    footers, or highlighted sections.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initialize the Inside filter.

        This constructor sets up the filter to capture events that correspond to content located
        inside a specific rectangular region, as defined by the provided coordinates (x, y) and
        dimensions (width, height). The filter allows subsequent event processing to focus on content
        within the defined area, enabling selective handling of content based on its position.

        :param x:       The x-coordinate of the lower-left corner of the rectangular area.
        :param y:       The y-coordinate of the lower-left corner of the rectangular area.
        :param width:   The width of the rectangular area.
        :param height:  The height of the rectangular area.
        """
        super().__init__()
        self.__x: int = x
        self.__y: int = y
        self.__width: int = width
        self.__height: int = height

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
        # IF there is no next Pipe
        # THEN return
        next_pipe: typing.Optional[Pipe] = self.get_next()
        if next_pipe is None:
            return

        # IF the event is within the specified bounds
        # THEN pass the event
        from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
        from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
        from borb.pdf.toolkit.source.event.image_event import ImageEvent
        from borb.pdf.toolkit.source.event.text_event import TextEvent

        if (
            isinstance(event, ShapeFillEvent)
            or isinstance(event, ShapeStrokeEvent)
            or isinstance(event, ImageEvent)
            or isinstance(event, TextEvent)
        ) and (
            (event.get_y() >= self.__y)
            and (event.get_y() + event.get_height() <= self.__y + self.__height)
            and (event.get_x() >= event.get_x())
            and (event.get_x() + event.get_width() <= self.__x + self.__width)
        ):
            next_pipe.process(event)
