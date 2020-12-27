from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextRise(CanvasOperator):
    """
    Set the text rise, T rise , to rise, which shall be a number expressed in
    unscaled text space units. Initial value: 0.
    """

    def __init__(self):
        super().__init__("Ts", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )
        canvas.graphics_state.text_rise = operands[0]
