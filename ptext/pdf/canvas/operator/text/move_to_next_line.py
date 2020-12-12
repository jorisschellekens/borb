from typing import List

from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.pdf.canvas.operator.text.move_text_position import MoveTextPosition
from ptext.io.tokenize.types.pdf_number import PDFFloat
from ptext.io.tokenize.types.pdf_object import PDFObject


class MoveToNextLine(CanvasOperator):
    """
    Move to the start of the next line. This operator has the same effect as the
    code
    0 -Tl Td
    where Tl denotes the current leading parameter in the text state. The
    negative of Tl is used here because Tl is the text leading expressed as a
    positive number. Going to the next line entails decreasing the
    y coordinate.
    """

    def __init__(self):
        super().__init__("T*", 0)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        operands = [PDFFloat(0), PDFFloat(-canvas.graphics_state.leading)]
        MoveTextPosition().invoke(canvas, operands)
