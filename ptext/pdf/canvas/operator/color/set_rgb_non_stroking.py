from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.color.color import RGBColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.tokenize.types.pdf_object import PDFObject


class SetRGBNonStroking(CanvasOperator):
    """
    Same as RG but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("rg", 3)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject]):
        for i in range(0, 3):
            if not isinstance(operands[i], PDFNumber):
                raise PDFTypeError(
                    expected_type=PDFNumber, received_type=operands[i].__class__
                )
        r = operands[0].get_decimal_value()
        g = operands[1].get_decimal_value()
        b = operands[2].get_decimal_value()
        canvas.graphics_state.non_stroke_color = RGBColor(r, g, b)
