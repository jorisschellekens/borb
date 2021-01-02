from decimal import Decimal
from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.color.color import CMYKColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetCMYKNonStroking(CanvasOperator):
    """
    Same as K but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("k", 4)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        assert isinstance(operands[3], Decimal)
        c = operands[0]
        m = operands[1]
        y = operands[2]
        k = operands[3]
        canvas.graphics_state.non_stroke_color = CMYKColor(c, m, y, k)
