from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.color.color import CMYKColor
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetCMYKStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceCMYK (or the DefaultCMYK
    colour space; see 8.6.5.6, "Default Colour Spaces") and set the colour to
    use for stroking operations. Each operand shall be a number between 0.0
    (zero concentration) and 1.0 (maximum concentration). The behaviour of
    this operator is affected by the overprint mode (see 8.6.7, "Overprint
    Control").
    """

    def __init__(self):
        super().__init__("K", 4)

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
        canvas.graphics_state.stroke_color = CMYKColor(c, m, y, k)
