#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Close the current subpath by appending a straight line
segment from the current point to the starting point of the
subpath. If the current subpath is already closed, h shall do
nothing.
"""

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.geometry.line_segment import LineSegment
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class CloseSubpath(CanvasOperator):
    """
    Close the current subpath by appending a straight line
    segment from the current point to the starting point of the
    subpath. If the current subpath is already closed, h shall do
    nothing.

    This operator terminates the current subpath. Appending
    another segment to the current path shall begin a new
    subpath, even if the new segment begins at the endpoint
    reached by the h operation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("h", 0)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the h operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """

        # get graphic state
        canvas = canvas_stream_processor.get_canvas()
        gs = canvas.graphics_state

        # path is empty
        if len(gs.path) == 0:
            return

        # first point in subpath
        x0 = gs.path[0].x0
        y0 = gs.path[0].y0

        # last point in subpath
        xn = gs.path[-1].x1
        yn = gs.path[-1].y1

        # append straight line segment
        gs.path.append(LineSegment(x0, y0, xn, yn))
