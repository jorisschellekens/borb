from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.color.color import GrayColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetGrayNonStroking(CanvasOperator):
    """
    Same as G but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("g", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        canvas.graphics_state.non_stroke_color = GrayColor(operands[0])
