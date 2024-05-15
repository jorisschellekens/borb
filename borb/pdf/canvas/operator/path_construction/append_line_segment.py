#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Append a straight line segment from the current point to the
point (x, y). The new current point shall be (x, y).
"""

import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.geometry.line_segment import LineSegment
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class AppendLineSegment(CanvasOperator):
    """
    Append a straight line segment from the current point to the
    point (x, y). The new current point shall be (x, y).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("l", 2)

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
        Invokes the l operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        assert isinstance(
            operands[0], Decimal
        ), "operand 0 of l operator must be of type Decimal"
        assert isinstance(
            operands[1], Decimal
        ), "operand 1 of l operator must be of type Decimal"

        # get graphic state
        canvas = canvas_stream_processor.get_canvas()
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # append all paths
        x0 = gs.path[-1].x1
        y0 = gs.path[-1].y1
        gs.path.append(LineSegment(x0, y0, operands[0], operands[1]))
