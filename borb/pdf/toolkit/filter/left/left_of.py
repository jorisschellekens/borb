#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content that appears to the left of a specified coordinate on the PDF page.

The `LeftOf` filter identifies and processes elements that are located to the left of
a defined x-coordinate threshold. This can be useful for extracting or manipulating content
within a specific horizontal region of the page, such as filtering out text or objects that
appear to the left of a particular point.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.image_event import ImageEvent
from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
from borb.pdf.toolkit.source.event.text_event import TextEvent


class LeftOf(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content that appears to the left of a specified coordinate on the PDF page.

    The `LeftOf` filter identifies and processes elements that are located to the left of
    a defined x-coordinate threshold. This can be useful for extracting or manipulating content
    within a specific horizontal region of the page, such as filtering out text or objects that
    appear to the left of a particular point.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(self, x: int):
        """
        Initialize a new instance of the `LeftOf` filter.

        :param x: The x-coordinate threshold for filtering. Only elements located left of
                  this value will be processed.
        """
        super().__init__()
        self.__x: int = x

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
        ) and event.get_x() <= self.__x:
            next_pipe.process(event)
