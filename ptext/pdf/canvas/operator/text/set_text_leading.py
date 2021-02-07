from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextLeading(CanvasOperator):
    """
    Set the text leading, T l , to leading, which shall be a number expressed in
    unscaled text space units. Text leading shall be used only by the T*, ', and
    " operators. Initial value: 0.
    """

    def __init__(self):
        super().__init__("TL", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        canvas.graphics_state.leading = operands[0]
