from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.geometry.line_segment import LineSegment
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class BeginSubpath(CanvasOperator):
    """
    Begin a new subpath by moving the current point to
    coordinates (x, y), omitting any connecting line segment. If
    the previous path construction operator in the current path
    was also m, the new m overrides it; no vestige of the
    previous m operation remains in the path.
    """

    def __init__(self):
        super().__init__("m", 2)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)

        # get graphic state
        gs = canvas.graphics_state

        # start empty subpath
        gs.path.append(LineSegment(operands[0], operands[1], operands[0], operands[1]))
