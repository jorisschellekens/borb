from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.object.canvas.operator.text.move_text_position import MoveTextPosition
from ptext.object.canvas.operator.text.set_text_leading import SetTextLeading
from ptext.primitive.pdf_number import PDFFloat, PDFNumber
from ptext.primitive.pdf_object import PDFObject


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

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):

        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )
        if not isinstance(operands[1], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[1].__class__
            )

        tx = operands[0].get_float_value()
        ty = operands[1].get_float_value()

        SetTextLeading().invoke(canvas, [PDFFloat(-ty)])
        MoveTextPosition().invoke(canvas, operands)
