#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener acts as a filter for other EventListener implementations.
    It only allows events to pass if they occur in a given Rectangle.
"""
import typing

from ptext.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from ptext.pdf.canvas.event.event_listener import Event, EventListener
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.geometry.rectangle import Rectangle


class LocationFilter(EventListener):
    """
    This implementation of EventListener acts as a filter for other EventListener implementations.
    It only allows events to pass if they occur in a given Rectangle.
    """

    def __init__(self, rectangle: Rectangle):
        self.rectangle = rectangle
        self.listeners: typing.List[EventListener] = []

    def add_listener(self, listener: "EventListener") -> "LocationFilter":
        """
        This methods add an EventListener to this (meta)-EventListener
        """
        self.listeners.append(listener)
        return self

    def _event_occurred(self, event: "Event") -> None:
        # filter ChunkOfTextRenderEvent
        if isinstance(event, ChunkOfTextRenderEvent):
            bb: typing.Optional[Rectangle] = event.get_bounding_box()
            assert bb is not None
            if self.rectangle.x < bb.x < (
                self.rectangle.x + self.rectangle.width
            ) and self.rectangle.y < bb.y < (self.rectangle.y + self.rectangle.height):
                for l in self.listeners:
                    l._event_occurred(event)
            return

        # filter ImageRenderEvent
        if isinstance(event, ImageRenderEvent):
            if self.rectangle.get_x() < event.get_x() < (
                self.rectangle.get_x() + self.rectangle.get_width()
            ) and self.rectangle.get_y() < event.get_y() < (
                self.rectangle.get_y() + self.rectangle.get_height()
            ):
                for l in self.listeners:
                    l._event_occurred(event)
            return

        # default
        for l in self.listeners:
            l._event_occurred(event)
