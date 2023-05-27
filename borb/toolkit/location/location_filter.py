#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener acts as a filter for other EventListener implementations.
    It only allows events to pass if they occur in a given Rectangle.
"""
import typing

from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle


class LocationFilter(EventListener):
    """
    This implementation of EventListener acts as a filter for other EventListener implementations.
    It only allows events to pass if they occur in a given Rectangle.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, rectangle: Rectangle):
        self._rectangle = rectangle
        self._listeners: typing.List[EventListener] = []

    #
    # PRIVATE
    #

    def _event_occurred(self, event: "Event") -> None:
        # filter ChunkOfTextRenderEvent
        if isinstance(event, ChunkOfTextRenderEvent):
            for glyph_event in event.split_on_glyphs():
                bb: typing.Optional[Rectangle] = glyph_event.get_previous_layout_box()
                assert bb is not None
                if self._rectangle.x < bb.x < (
                    self._rectangle.x + self._rectangle.width
                ) and self._rectangle.y < bb.y < (
                    self._rectangle.y + self._rectangle.height
                ):
                    for l in self._listeners:
                        l._event_occurred(glyph_event)
            return

        # filter ImageRenderEvent
        if isinstance(event, ImageRenderEvent):
            if self._rectangle.get_x() < event.get_x() < (
                self._rectangle.get_x() + self._rectangle.get_width()
            ) and self._rectangle.get_y() < event.get_y() < (
                self._rectangle.get_y() + self._rectangle.get_height()
            ):
                for l in self._listeners:
                    l._event_occurred(event)
            return

        # default
        for l in self._listeners:
            l._event_occurred(event)

    #
    # PUBLIC
    #

    def add_listener(self, listener: "EventListener") -> "LocationFilter":
        """
        This methods add an EventListener to this (meta)-EventListener
        """
        self._listeners.append(listener)
        return self
