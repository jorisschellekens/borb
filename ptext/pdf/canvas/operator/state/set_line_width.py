from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.tokenize.types.pdf_object import PDFObject


class SetLineWidth(CanvasOperator):
    """
    Set the line width in the graphics state (see 8.4.3.2, "Line Width").
    """

    def __init__(self):
        super().__init__("w", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )
        canvas.graphics_state.line_width = operands[0].get_decimal_value()
