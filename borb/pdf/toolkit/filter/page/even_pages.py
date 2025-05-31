#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A processing pipe that forwards events only for even-numbered pages in a PDF.

This class extends the `Pipe` class and filters events based on the page number.
If the page associated with the event is even-numbered, the event is forwarded to the next pipe in the processing chain.
Otherwise, the event is discarded.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe


class EvenPages(Pipe):
    """
    A processing pipe that forwards events only for even-numbered pages in a PDF.

    This class extends the `Pipe` class and filters events based on the page number.
    If the page associated with the event is even-numbered, the event is forwarded to the next pipe in the processing chain.
    Otherwise, the event is discarded.
    """

    #
    # CONSTRUCTOR
    #

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

        # push to next pipe
        page_nr: int = event.get_page_nr()
        if (page_nr != -1) and (page_nr % 2 == 0):
            next_pipe.process(event)
