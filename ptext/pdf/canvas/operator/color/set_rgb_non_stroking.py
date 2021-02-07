from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.color.color import RGBColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetRGBNonStroking(CanvasOperator):
    """
    Same as RG but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("rg", 3)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        r = operands[0]
        g = operands[1]
        b = operands[2]
        canvas.graphics_state.non_stroke_color = RGBColor(r, g, b)
