from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.color.color import GrayColor
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetGrayNonStroking(CanvasOperator):
    """
    Same as G but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("g", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject]):
        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )
        g = operands[0].get_float_value()
        canvas.graphics_state.non_stroke_color = GrayColor(g)
