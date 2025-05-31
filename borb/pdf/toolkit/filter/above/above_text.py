#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams to retain content positioned visually above a specified text element on the page.

`AboveText` extends `PageContentStreamFilter` to provide targeted filtering of
content that appears above a specified text (e.g., "Lorem Ipsum") in the document's
content stream. This can be useful in document processing tasks where context-specific
content separation is needed, such as extracting headers, annotations, or images
that are positioned above specific keywords or phrases.
"""
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe


class AboveText(Pipe):
    """
    A filter class for processing PDF page content streams to retain content positioned visually above a specified text element on the page.

    `AboveText` extends `PageContentStreamFilter` to provide targeted filtering of
    content that appears above a specified text (e.g., "Lorem Ipsum") in the document's
    content stream. This can be useful in document processing tasks where context-specific
    content separation is needed, such as extracting headers, annotations, or images
    that are positioned above specific keywords or phrases.
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
