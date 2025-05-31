#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF content streams, targeting content positioned above a specified y-coordinate on the page.

The `Above` class extends `PageContentStreamFilter` and is used to filter and modify
page content streams based on vertical positioning, allowing only the content above a
specified threshold (typically a y-coordinate) to be retained in the filtered stream.

This functionality is useful for applications that need to analyze or manipulate portions
of the page content based on layout requirements. For example, extracting header sections,
content above a certain y-coordinate, or portions of text/images that appear in the
upper part of a page.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.image_event import ImageEvent
from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
from borb.pdf.toolkit.source.event.text_event import TextEvent


class Above(Pipe):
    """
    A filter class for processing PDF content streams, targeting content positioned above a specified y-coordinate on the page.

    The `Above` class extends `PageContentStreamFilter` and is used to filter and modify
    page content streams based on vertical positioning, allowing only the content above a
    specified threshold (typically a y-coordinate) to be retained in the filtered stream.

    This functionality is useful for applications that need to analyze or manipulate portions
    of the page content based on layout requirements. For example, extracting header sections,
    content above a certain y-coordinate, or portions of text/images that appear in the
    upper part of a page.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, y: int):
        """
        Initialize a new instance of the `Above` filter.

        :param y: The y-coordinate threshold for filtering. Only elements located above
                  this value will be processed.
        """
        super().__init__()
        self.__y: int = y

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def process(
        self,
        event: Event,
    ):
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

        # pass along to the next Pipe
        if (
            isinstance(event, ShapeFillEvent)
            or isinstance(event, ShapeStrokeEvent)
            or isinstance(event, ImageEvent)
            or isinstance(event, TextEvent)
        ) and event.get_y() >= self.__y:
            next_pipe.process(event)
