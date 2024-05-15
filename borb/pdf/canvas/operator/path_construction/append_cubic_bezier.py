#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Bézier curve is a parametric curve used in computer graphics and related fields.
The curve, which is related to the Bernstein polynomial, is named after Pierre Bézier,
who used it in the 1960s for designing curves for the bodywork of Renault cars.
Other uses include the design of computer fonts and animation.
Bézier curves can be combined to form a Bézier spline, or generalized to higher dimensions to form Bézier surfaces.
The Bézier triangle is a special case of the latter.
"""

import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.geometry.line_segment import LineSegment
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


def _bezier(p0, p1, p2, p3) -> typing.List[LineSegment]:
    pts = []
    ONE = Decimal(1)
    for t in [
        Decimal(x) for x in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    ]:
        x = (
            (ONE - t) ** 3 * p0[0]
            + 3 * t * (ONE - t) ** 2 * p1[0]
            + 3 * t ** 2 * (ONE - t) * p2[0]
            + t ** 3 * p3[0]
        )
        y = (
            (ONE - t) ** 3 * p0[1]
            + 3 * t * (ONE - t) ** 2 * p1[1]
            + 3 * t ** 2 * (ONE - t) * p2[1]
            + t ** 3 * p3[1]
        )
        pts.append((x, y))

    # build List of LineSegments
    out: typing.List[LineSegment] = []
    for i in range(1, len(pts)):
        out.append(LineSegment(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1]))

    # return
    return out


class AppendCubicBezierCurve1(CanvasOperator):
    """
    Append a cubic Bézier curve to the current path. The curve
    shall extend from the current point to the point (x3 , y3 ), using
    (x1 , y1 ) and (x2 , y2 ) as the Bézier control points (see 8.5.2.2,
    "Cubic Bézier Curves"). The new current point shall be
    (x3 , y3 ).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("c", 6)

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
        Invokes the c operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        assert isinstance(
            operands[0], Decimal
        ), "operand 0 of c operator must be of type Decimal"
        assert isinstance(
            operands[1], Decimal
        ), "operand 1 of c operator must be of type Decimal"
        assert isinstance(
            operands[2], Decimal
        ), "operand 2 of c operator must be of type Decimal"
        assert isinstance(
            operands[3], Decimal
        ), "operand 3 of c operator must be of type Decimal"
        assert isinstance(
            operands[4], Decimal
        ), "operand 4 of c operator must be of type Decimal"
        assert isinstance(
            operands[5], Decimal
        ), "operand 5 of c operator must be of type Decimal"

        # get graphic state
        canvas = canvas_stream_processor.get_canvas()
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # build control points
        p0 = (gs.path[-1].x1, gs.path[-1].y1)
        p1 = (operands[0], operands[1])
        p2 = (operands[2], operands[3])
        p3 = (operands[4], operands[5])

        # append all paths
        for l in _bezier(p0, p1, p2, p3):
            gs.path.append(l)


class AppendCubicBezierCurve2(CanvasOperator):
    """
    Append a cubic Bézier curve to the current path. The curve
    shall extend from the current point to the point (x3 , y3 ), using
    the current point and (x2 , y2 ) as the Bézier control points (see
    8.5.2.2, "Cubic Bézier Curves"). The new current point shall
    be (x3 , y3 ).
    """

    def __init__(self):
        super().__init__("v", 4)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invokes the v operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        assert isinstance(
            operands[0], Decimal
        ), "operand 0 of v operator must be of type Decimal"
        assert isinstance(
            operands[1], Decimal
        ), "operand 1 of v operator must be of type Decimal"
        assert isinstance(
            operands[2], Decimal
        ), "operand 2 of v operator must be of type Decimal"
        assert isinstance(
            operands[3], Decimal
        ), "operand 3 of v operator must be of type Decimal"

        # get graphic state
        canvas = canvas_stream_processor.get_canvas()
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # build control points
        p0 = (gs.path[-1].x1, gs.path[-1].y1)
        p1 = p0
        p2 = (operands[0], operands[1])
        p3 = (operands[2], operands[3])

        # append all paths
        for l in _bezier(p0, p1, p2, p3):
            gs.path.append(l)


class AppendCubicBezierCurve3(CanvasOperator):
    """
    Append a cubic Bézier curve to the current path. The curve
    shall extend from the current point to the point (x3 , y3 ), using
    (x1 , y1 ) and (x3 , y3 ) as the Bézier control points (see 8.5.2.2,
    "Cubic Bézier Curves"). The new current point shall be (x3 , y3 ).
    """

    def __init__(self):
        super().__init__("y", 4)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invokes the y operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        assert isinstance(
            operands[0], Decimal
        ), "operand 0 of y operator must be of type Decimal"
        assert isinstance(
            operands[1], Decimal
        ), "operand 1 of y operator must be of type Decimal"
        assert isinstance(
            operands[2], Decimal
        ), "operand 2 of y operator must be of type Decimal"
        assert isinstance(
            operands[3], Decimal
        ), "operand 3 of y operator must be of type Decimal"

        # get graphic state
        canvas = canvas_stream_processor.get_canvas()
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # build control points
        p0 = (gs.path[-1].x1, gs.path[-1].y1)
        p1 = (operands[0], operands[1])
        p2 = (operands[2], operands[3])
        p3 = p2

        # append all paths
        for l in _bezier(p0, p1, p2, p3):
            gs.path.append(l)
