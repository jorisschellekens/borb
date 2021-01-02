from decimal import Decimal
from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextRise(CanvasOperator):
    """
    Set the text rise, T rise , to rise, which shall be a number expressed in
    unscaled text space units. Initial value: 0.
    """

    def __init__(self):
        super().__init__("Ts", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        canvas.graphics_state.text_rise = operands[0]
