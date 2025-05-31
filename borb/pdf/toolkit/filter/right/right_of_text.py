#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content that appears to the right of a specified text string on the PDF page.

The `RightOfText` filter identifies and processes elements located to the right of a
given text string on the page. This can be useful for filtering or manipulating content
that appears next to or after a specific text, such as extracting text or objects located
to the right of a particular word or phrase.
"""
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe


class RightOfText(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content that appears to the right of a specified text string on the PDF page.

    The `RightOfText` filter identifies and processes elements located to the right of a
    given text string on the page. This can be useful for filtering or manipulating content
    that appears next to or after a specific text, such as extracting text or objects located
    to the right of a particular word or phrase.
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
        pass
