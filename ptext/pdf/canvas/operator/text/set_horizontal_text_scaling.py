from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.tokenize.types.pdf_object import PDFObject


class SetHorizontalScaling(CanvasOperator):
    """
    Set the horizontal scaling, Th , to (scale ÷ 100). scale shall be a number
    specifying the percentage of the normal width. Initial value: 100 (normal
    width).
    """

    def __init__(self):
        super().__init__("Tz", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):

        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )

        canvas.graphics_state.horizontal_scaling = operands[0].get_decimal_value()
