#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content that appears below a specified text reference on the PDF page.

This filter identifies and processes elements, typically text or images, that are
positioned beneath a designated text phrase or string within the content stream.
By setting a reference text, `BelowText` allows selective extraction, manipulation,
or analysis of content appearing below that text. This is particularly useful in
document workflows where spatial relationships relative to text references are significant.
"""
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe


class BelowText(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content that appears below a specified text reference on the PDF page.

    This filter identifies and processes elements, typically text or images, that are
    positioned beneath a designated text phrase or string within the content stream.
    By setting a reference text, `BelowText` allows selective extraction, manipulation,
    or analysis of content appearing below that text. This is particularly useful in
    document workflows where spatial relationships relative to text references are significant.
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
