from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetLineWidth(CanvasOperator):
    """
    Set the line width in the graphics state (see 8.4.3.2, "Line Width").
    """

    def __init__(self):
        super().__init__("w", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )
        canvas.graphics_state.line_width = operands[0]
