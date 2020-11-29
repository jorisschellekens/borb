from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetCharacterSpacing(CanvasOperator):
    """
    Set the character spacing, Tc , to charSpace, which shall be a number
    expressed in unscaled text space units. Character spacing shall be used
    by the Tj, TJ, and ' operators. Initial value: 0.
    """

    def __init__(self):
        super().__init__("Tc", 1)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):

        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )

        canvas.graphics_state.character_spacing = operands[0].get_decimal_value()
