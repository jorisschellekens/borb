#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A debug utility that draws a bounding box around specific (text) events.

This class processes text rendering events and overlays a red rectangle around
selected instances of (text) event(s). The user can specify which (text) events to highlight
by providing a list of indices.
"""
import typing

from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.sink.sink import Sink
from borb.pdf.toolkit.source.event.text_event import TextEvent


class DrawBoundingBoxes(Sink):
    """
    A debug utility that draws a bounding box around specific (text) events.

    This class processes text rendering events and overlays a red rectangle around
    selected instances of (text) event(s). The user can specify which (text) events to highlight
    by providing a list of indices.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(self, text_event_indices_to_mark: typing.List[int] = []):
        """Initialize the DrawBoundingBoxes instance."""
        super().__init__()
        self.__count: int = -1
        self.__event_indices_to_mark: typing.List[int] = text_event_indices_to_mark

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

        if len(event.get_text().strip()) == 0:
            return

        self.__count += 1

        # TODO: use calculated height
        event._TextEvent__height = 10  # type: ignore[attr-defined]

        # render
        if self.__count in self.__event_indices_to_mark:
            Shape(
                coordinates=[
                    (0, 0),
                    (0, event.get_height()),
                    (event.get_width(), event.get_height()),
                    (event.get_width(), 0),
                    (0, 0),
                ],
                stroke_color=X11Color.RED,
            ).paint(
                available_space=(
                    int(event.get_x()),
                    int(event.get_y()),
                    int(event.get_width()),
                    int(event.get_height()),
                ),
                page=event.get_page(),
            )
