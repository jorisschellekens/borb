from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.color.color import RGBColor
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetRGBStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceRGB (or the DefaultRGB colour
    space; see 8.6.5.6, "Default Colour Spaces") and set the colour to use for
    stroking operations. Each operand shall be a number between 0.0
    (minimum intensity) and 1.0 (maximum intensity).
    """

    def __init__(self):
        super().__init__("RG", 3)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject]):
        for i in range(0, 3):
            if not isinstance(operands[i], PDFNumber):
                raise PDFTypeError(
                    expected_type=PDFNumber, received_type=operands[i].__class__
                )
        r = operands[0].get_float_value()
        g = operands[1].get_float_value()
        b = operands[2].get_float_value()
        canvas.graphics_state.stroke_color = RGBColor(r, g, b)
