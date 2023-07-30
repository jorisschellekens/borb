#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener acts as a filter for other EventListener implementations.
    It only allows events to pass if they occur in a given Rectangle.
"""
import typing
from decimal import Decimal

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener


class FontColorFilter(EventListener):
    """
    This implementation of EventListener acts as a filter for other EventListener implementations.
    It only allows ChunkOfTextRenderEvent to pass if their corresponding color matches.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, color: Color, maximum_normalized_rgb_distance: Decimal):
        self._color: RGBColor = color.to_rgb()
        assert Decimal(0) <= maximum_normalized_rgb_distance <= Decimal(1)
        self._maximum_normalized_rgb_distance = maximum_normalized_rgb_distance
        self._listeners: typing.List[EventListener] = []

    #
    # PRIVATE
    #

    def _event_occurred(self, event: "Event") -> None:
        # filter ChunkOfTextRenderEvent
        if isinstance(event, ChunkOfTextRenderEvent):
            font_color: Color = event.get_font_color()
            rgb_font_color: RGBColor = font_color.to_rgb()
            color_distance: Decimal = (
                (rgb_font_color.red - self._color.red) ** 2
                + (rgb_font_color.green - self._color.green) ** 2
                + (rgb_font_color.blue - self._color.blue) ** 2
            ) / 3
            if color_distance <= self._maximum_normalized_rgb_distance:
                for l in self._listeners:
                    l._event_occurred(event)
            return
        # default
        for l in self._listeners:
            l._event_occurred(event)

    #
    # PUBLIC
    #

    def add_listener(self, listener: "EventListener") -> "FontColorFilter":
        """
        This methods add an EventListener to this (meta)-EventListener
        """
        self._listeners.append(listener)
        return self
