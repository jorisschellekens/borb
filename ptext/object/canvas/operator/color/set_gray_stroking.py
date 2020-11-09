from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.color.color import GrayColor
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetGrayStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceGray (or the DefaultGray colour
    space; see 8.6.5.6, "Default Colour Spaces") and set the gray level to use
    for stroking operations. gray shall be a number between 0.0 (black) and
    1.0 (white).
    """

    def __init__(self):
        super().__init__("G", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject]):
        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )
        g = operands[0].get_float_value()
        canvas.graphics_state.stroke_color = GrayColor(g)
