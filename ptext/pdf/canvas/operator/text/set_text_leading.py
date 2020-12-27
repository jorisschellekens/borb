from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextLeading(CanvasOperator):
    """
    Set the text leading, T l , to leading, which shall be a number expressed in
    unscaled text space units. Text leading shall be used only by the T*, ', and
    " operators. Initial value: 0.
    """

    def __init__(self):
        super().__init__("TL", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )

        canvas.graphics_state.leading = operands[0]
