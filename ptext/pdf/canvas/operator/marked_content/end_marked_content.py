from typing import List

from ptext.exception.pdf_exception import IllegalGraphicsStateError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class EndMarkedContent(CanvasOperator):
    """
    End a marked-content sequence begun by a BMC or BDC operator.
    """

    def __init__(self):
        super().__init__("EMC", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        if len(canvas.marked_content_stack) == 0:
            raise IllegalGraphicsStateError(
                message="unable to execute operator %s, canvas tag hierarchy is currently empty"
                % (self.text,)
            )
        canvas.marked_content_stack.pop(-1)
