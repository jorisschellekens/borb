from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetWordSpacing(CanvasOperator):
    """
    Set the word spacing, T w , to wordSpace, which shall be a number
    expressed in unscaled text space units. Word spacing shall be used by
    the Tj, TJ, and ' operators. Initial value: 0.
    """

    def __init__(self):
        super().__init__("Tw", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )
        canvas.graphics_state.word_spacing = operands[0].get_decimal_value()
