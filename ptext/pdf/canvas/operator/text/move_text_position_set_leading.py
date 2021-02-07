from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.pdf.canvas.operator.text.move_text_position import MoveTextPosition
from ptext.pdf.canvas.operator.text.set_text_leading import SetTextLeading


class MoveTextPositionSetLeading(CanvasOperator):
    """
    Move to the start of the next line, offset from the start of the current line by
    (tx , ty). As a side effect, this operator shall set the leading parameter in
    the text state. This operator shall have the same effect as this code:
    −ty TL
    tx ty Td
    """

    def __init__(self):
        super().__init__("TD", 2)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]

        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)

        SetTextLeading().invoke(canvas, [-operands[1]])
        MoveTextPosition().invoke(canvas, operands)
