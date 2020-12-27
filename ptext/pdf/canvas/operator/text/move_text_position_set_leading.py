from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
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

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):

        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )
        if not isinstance(operands[1], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[1].__class__
            )

        tx = operands[0]
        ty = operands[1]

        SetTextLeading().invoke(canvas, [-ty])
        MoveTextPosition().invoke(canvas, operands)
