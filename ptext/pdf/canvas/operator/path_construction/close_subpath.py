from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.geometry.line_segment import LineSegment
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


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

    def __init__(self):
        super().__init__("h", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]

        # get graphic state
        gs = canvas.graphics_state

        # path should not be empty
        assert len(gs.path) > 0

        # first point in subpath
        x0 = gs.path[0].x0
        y0 = gs.path[0].y0

        # last point in subpath
        xn = gs.path[-1].x1
        yn = gs.path[-1].y1

        # append straight line segment
        gs.path.append(LineSegment(x0, y0, xn, yn))
