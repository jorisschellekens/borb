from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetWordSpacing(CanvasOperator):
    """
    Set the word spacing, T w , to wordSpace, which shall be a number
    expressed in unscaled text space units. Word spacing shall be used by
    the Tj, TJ, and ' operators. Initial value: 0.
    """

    def __init__(self):
        super().__init__("Tw", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )
        canvas.graphics_state.word_spacing = operands[0]
