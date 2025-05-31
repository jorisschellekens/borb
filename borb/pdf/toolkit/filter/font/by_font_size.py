#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting text content rendered in a specified font size.

This filter identifies and processes text elements based on their font size, allowing selective
extraction or manipulation of text segments that match a given size. `ByFontSize` is useful for
handling content where text size denotes hierarchy or emphasis, such as headings, subheadings, or
body text in structured documents.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.text_event import TextEvent


class ByFontSize(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting text content rendered in a specified font size.

    This filter identifies and processes text elements based on their font size, allowing selective
    extraction or manipulation of text segments that match a given size. `ByFontSize` is useful for
    handling content where text size denotes hierarchy or emphasis, such as headings, subheadings, or
    body text in structured documents.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        max_font_size: typing.Optional[int] = None,
        min_font_size: typing.Optional[int] = None,
    ):
        """
        Initialize a new instance of the `ByFontSize` filter.

        :param max_font_size: The maximum font size to filter for. Defaults to the largest possible integer if not specified.
        :param min_font_size: The minimum font size to filter for. Defaults to 0 if not specified.
        """
        super().__init__()
        self.__max_font_size: int = max_font_size or (2**32)
        self.__min_font_size: int = min_font_size or 0

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
        if not isinstance(event, TextEvent):
            return

        # IF the font_color does not match
        # THEN return
        if event.get_font_size() < self.__min_font_size:
            return
        if event.get_font_size() > self.__max_font_size:
            return

        # IF there is no next Pipe
        # THEN return
        next_pipe: typing.Optional[Pipe] = self.get_next()
        if next_pipe is None:
            return

        # pass along to the next Pipe
        next_pipe.process(event)
