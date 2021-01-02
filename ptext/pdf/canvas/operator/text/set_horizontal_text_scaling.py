from decimal import Decimal
from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetHorizontalScaling(CanvasOperator):
    """
    Set the horizontal scaling, Th , to (scale ÷ 100). scale shall be a number
    specifying the percentage of the normal width. Initial value: 100 (normal
    width).
    """

    def __init__(self):
        super().__init__("Tz", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        canvas.graphics_state.horizontal_scaling = operands[0]
