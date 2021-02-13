from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.event.begin_text_event import BeginTextEvent
from ptext.pdf.canvas.geometry.matrix import Matrix
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class BeginTextObject(CanvasOperator):
    """
    Begin a text object, initializing the text matrix, Tm , and the text line matrix,
    Tlm , to the identity matrix. Text objects shall not be nested; a second BT shall
    not appear before an ET.
    """

    def __init__(self):
        super().__init__("BT", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        """
        Invoke the BT operator
        """
        canvas.graphics_state.text_matrix = Matrix.identity_matrix()
        canvas.graphics_state.text_line_matrix = Matrix.identity_matrix()
        canvas.event_occurred(BeginTextEvent())
