from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.color.color import CMYKColor
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetCMYKNonStroking(CanvasOperator):
    """
    Same as K but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("k", 4)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject]):
        for i in range(0, 4):
            if not isinstance(operands[i], PDFNumber):
                raise PDFTypeError(
                    expected_type=PDFNumber, received_type=operands[i].__class__
                )
        c = operands[0].get_decimal_value()
        m = operands[1].get_decimal_value()
        y = operands[2].get_decimal_value()
        k = operands[3].get_decimal_value()
        canvas.graphics_state.non_stroke_color = CMYKColor(c, m, y, k)
