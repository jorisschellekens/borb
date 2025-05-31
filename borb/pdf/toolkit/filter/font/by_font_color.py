#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A filter class for processing PDF page content streams, specifically targeting text content rendered in a specified font color.

This filter identifies and processes text elements based on their color, allowing selective
extraction or manipulation of text segments that match a particular color code (e.g., RGB values).
`ByFontColor` is useful for distinguishing different types of information or emphasis in documents
where color is used to signify importance, categorization, or grouping of text.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.pipe import Pipe
from borb.pdf.toolkit.source.event.text_event import TextEvent


class ByFontColor(Pipe):
    """
    A filter class for processing PDF page content streams, specifically targeting text content rendered in a specified font color.

    This filter identifies and processes text elements based on their color, allowing selective
    extraction or manipulation of text segments that match a particular color code (e.g., RGB values).
    `ByFontColor` is useful for distinguishing different types of information or emphasis in documents
    where color is used to signify importance, categorization, or grouping of text.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, font_color: Color):
        """
        Initialize a new instance of the `ByFontColor` filter.

        :param font_color: The font color to filter for. Text elements rendered using
                          this font color will be processed by this filter.
        """
        super().__init__()
        self.__font_color: Color = font_color

    #
    # PRIVATE
    #

    @staticmethod
    def __dist(c0: Color, c1: Color) -> float:
        r0: RGBColor = c0.to_rgb_color()
        r1: RGBColor = c1.to_rgb_color()
        delta: float = (r0.get_red() - r1.get_red()) ** 2
        delta += (r0.get_green() - r1.get_green()) ** 2
        delta += (r0.get_blue() - r1.get_blue()) ** 2
        delta = delta**0.5
        return delta

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
        # fmt: off
        normalized_color_distance: float = ByFontColor.__dist(self.__font_color, event.get_font_color()) / ByFontColor.__dist(X11Color.BLACK, X11Color.WHITE)
        if normalized_color_distance > 0.05:
            return
        # fmt: on

        # IF there is no next Pipe
        # THEN return
        next_pipe: typing.Optional[Pipe] = self.get_next()
        if next_pipe is None:
            return

        # pass along to the next Pipe
        next_pipe.process(event)
