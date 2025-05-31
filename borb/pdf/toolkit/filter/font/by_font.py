#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting content  associated with a specified font type.

This filter identifies and processes text elements rendered using a particular font,
allowing selective extraction, manipulation, or analysis based on font style, family,
or name. `ByFont` is especially useful in cases where different fonts in a document
denote different types of information, such as headings, footnotes, or emphasized text.
"""
import typing

from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.text_event import TextEvent


class ByFont(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting content  associated with a specified font type.

    This filter identifies and processes text elements rendered using a particular font,
    allowing selective extraction, manipulation, or analysis based on font style, family,
    or name. `ByFont` is especially useful in cases where different fonts in a document
    denote different types of information, such as headings, footnotes, or emphasized text.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, font_name: str):
        """
        Initialize a new instance of the `ByFont` filter.

        :param font_name: The name of the font to filter for. Text elements rendered using
                          this font will be processed by this filter.
        """
        super().__init__()
        self.__font_name: str = font_name

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

        # IF the font_name does not match
        # THEN return
        font_name: typing.Optional[str] = event.get_font().get("Name", None)
        if font_name != self.__font_name:
            return

        # IF there is no next Pipe
        # THEN return
        next_pipe: typing.Optional[Pipe] = self.get_next()
        if next_pipe is None:
            return

        # pass along to the next Pipe
        next_pipe.process(event)
