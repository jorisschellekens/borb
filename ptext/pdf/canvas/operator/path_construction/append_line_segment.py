#!/usr/bin/env python

from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.geometry.line_segment import LineSegment
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class AppendLineSegment(CanvasOperator):
    """
    Append a straight line segment from the current point to the
    point (x, y). The new current point shall be (x, y).
    """

    def __init__(self):
        super().__init__("l", 2)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invokes the l operator
        """
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)

        # get graphic state
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # append all paths
        x0 = gs.path[-1].x1
        y0 = gs.path[-1].y1
        gs.path.append(LineSegment(x0, y0, operands[0], operands[1]))
