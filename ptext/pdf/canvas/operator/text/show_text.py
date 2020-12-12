from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.event.text_render_event import TextRenderEvent
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_object import PDFObject
from ptext.io.tokenize.types.pdf_string import PDFString


class ShowText(CanvasOperator):
    """
    Show a text string.
    """

    def __init__(self):
        super().__init__("Tj", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if not isinstance(operands[0], PDFString):
            raise PDFTypeError(
                expected_type=PDFString, received_type=operands[0].__class__
            )
        tri = TextRenderEvent(canvas.graphics_state, operands[0])
        # render
        canvas.event_occurred(tri)
        # update text rendering location
        canvas.graphics_state.text_matrix[2][0] += tri.get_baseline().length()
