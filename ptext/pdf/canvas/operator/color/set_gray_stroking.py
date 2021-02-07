from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.color.color import GrayColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetGrayStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceGray (or the DefaultGray colour
    space; see 8.6.5.6, "Default Colour Spaces") and set the gray level to use
    for stroking operations. gray shall be a number between 0.0 (black) and
    1.0 (white).
    """

    def __init__(self):
        super().__init__("G", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        canvas.graphics_state.stroke_color = GrayColor(operands[0])
