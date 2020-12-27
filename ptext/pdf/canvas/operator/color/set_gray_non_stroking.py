from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.color.color import GrayColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetGrayNonStroking(CanvasOperator):
    """
    Same as G but used for nonstroking operations.
    """

    def __init__(self):
        super().__init__("g", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType]):
        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )
        g = operands[0]
        canvas.graphics_state.non_stroke_color = GrayColor(g)
