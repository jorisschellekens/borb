from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetHorizontalScaling(CanvasOperator):
    """
    Set the horizontal scaling, Th , to (scale ÷ 100). scale shall be a number
    specifying the percentage of the normal width. Initial value: 100 (normal
    width).
    """

    def __init__(self):
        super().__init__("Tz", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )

        canvas.graphics_state.horizontal_scaling = operands[0]
