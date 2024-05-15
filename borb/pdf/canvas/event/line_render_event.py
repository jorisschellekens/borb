#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered right after the Canvas has processed a stroke-path instruction.
"""
from borb.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.geometry.line_segment import LineSegment


class LineRenderEvent(Event):
    """
    This implementation of Event is triggered right after the Canvas has processed a stroke-path instruction.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, graphics_state: CanvasGraphicsState, line_segment: LineSegment):
        super(LineRenderEvent, self).__init__()
        self._graphics_state = graphics_state
        self._line_segment = line_segment

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_line_segment(self) -> LineSegment:
        """
        Get the LineSegment that was constructed through various path-painting operators
        :return:    the LineSegment
        """
        return self._line_segment
