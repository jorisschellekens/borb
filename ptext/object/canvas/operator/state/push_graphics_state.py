import copy
from typing import List

from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_object import PDFObject


class PushGraphicsState(CanvasOperator):
    """
    Save the current graphics state on the graphics state stack (see
    8.4.2, "Graphics State Stack").
    """

    def __init__(self):
        super().__init__("q", 0)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        canvas.graphics_state_stack.append(copy.deepcopy(canvas.graphics_state))
