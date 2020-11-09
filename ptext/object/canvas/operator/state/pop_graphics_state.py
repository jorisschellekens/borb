from typing import List

from ptext.exception.pdf_exception import IllegalGraphicsStateError
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_object import PDFObject


class PopGraphicsState(CanvasOperator):
    """
    Restore the graphics state by removing the most recently saved
    state from the stack and making it the current state (see 8.4.2,
    "Graphics State Stack").
    """

    def __init__(self):
        super().__init__("Q", 0)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if len(canvas.graphics_state_stack) == 0:
            raise IllegalGraphicsStateError(
                message="Not possible to execute Q operator. Graphics state is empty."
            )
        canvas.graphics_state = canvas.graphics_state_stack.pop(-1)
