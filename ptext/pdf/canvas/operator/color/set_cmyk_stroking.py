from decimal import Decimal
from typing import List

from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.color.color import CMYKColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetCMYKStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceCMYK (or the DefaultCMYK
    colour space; see 8.6.5.6, "Default Colour Spaces") and set the colour to
    use for stroking operations. Each operand shall be a number between 0.0
    (zero concentration) and 1.0 (maximum concentration). The behaviour of
    this operator is affected by the overprint mode (see 8.6.7, "Overprint
    Control").
    """

    def __init__(self):
        super().__init__("K", 4)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType]):
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        assert isinstance(operands[3], Decimal)
        c = operands[0]
        m = operands[1]
        y = operands[2]
        k = operands[3]
        canvas.graphics_state.stroke_color = CMYKColor(c, m, y, k)
