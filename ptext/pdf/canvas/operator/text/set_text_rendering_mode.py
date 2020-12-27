from typing import List

from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextRenderingMode(CanvasOperator):
    """
    Set the text rendering mode, T mode , to render, which shall be an integer.
    Initial value: 0.
    """

    def __init__(self):
        super().__init__("Tr", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        # TODO implement 'Tr' operator
        pass
