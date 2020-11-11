from typing import List

from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_object import PDFObject


class SetTextRenderingMode(CanvasOperator):
    """
    Set the text rendering mode, T mode , to render, which shall be an integer.
    Initial value: 0.
    """

    def __init__(self):
        super().__init__("Tr", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        # TODO implement 'Tr' operator
        pass
