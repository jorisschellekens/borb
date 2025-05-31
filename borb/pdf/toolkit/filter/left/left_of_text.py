#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content that appears to the left of a specified text within the PDF page.

The `LeftOfText` filter identifies and processes content that is positioned to the left
of a given text within the PDF page. This is useful for selectively extracting or manipulating
elements that appear to the left of specific textual content, allowing for precise targeting in
content extraction and manipulation.
"""
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe


class LeftOfText(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content that appears to the left of a specified text within the PDF page.

    The `LeftOfText` filter identifies and processes content that is positioned to the left
    of a given text within the PDF page. This is useful for selectively extracting or manipulating
    elements that appear to the left of specific textual content, allowing for precise targeting in
    content extraction and manipulation.
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
