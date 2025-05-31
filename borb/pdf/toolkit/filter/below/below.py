#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content that appears below a specified y-coordinate on the PDF page.

This class is part of a filtering system designed to handle and manipulate portions
of a PDF content stream based on their vertical position. Using `Below`, only
content located beneath the given y-coordinate threshold is targeted, allowing for
selective manipulation or extraction of content positioned lower on the page.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.image_event import ImageEvent
from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
from borb.pdf.toolkit.source.event.text_event import TextEvent


class Below(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content that appears below a specified y-coordinate on the PDF page.

    This class is part of a filtering system designed to handle and manipulate portions
    of a PDF content stream based on their vertical position. Using `Below`, only
    content located beneath the given y-coordinate threshold is targeted, allowing for
    selective manipulation or extraction of content positioned lower on the page.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, y: int):
        """
        Initialize a new instance of the `Below` filter.

        :param y: The y-coordinate threshold for filtering. Only elements located below
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
        ) and event.get_y() <= self.__y:
            next_pipe.process(event)
