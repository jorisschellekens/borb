from typing import List

from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.pdf.canvas.operator.text.move_to_next_line import MoveToNextLine
from ptext.pdf.canvas.operator.text.show_text import ShowText


class MoveToNextLineShowText(CanvasOperator):
    """
    Move to the next line and show a text string. This operator shall have the
    same effect as the code
    T*
    string Tj
    """

    def __init__(self):
        super().__init__("'", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        MoveToNextLine().invoke(canvas, [])
        ShowText().invoke(canvas, operands)
