from typing import List

from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_object import PDFObject


class EndCompatibilitySection(CanvasOperator):
    """
    (PDF 1.1) Begin a compatibility section. Unrecognized operators (along with
    their operands) shall be ignored without error until the balancing EX operator
    is encountered.
    """

    def __init__(self):
        super().__init__("EX", 0)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        canvas.in_compatibility_section = False
