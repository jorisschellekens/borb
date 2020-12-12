from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.pdf.canvas.geometry.matrix import Matrix
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator
from ptext.io.tokenize.types.pdf_number import PDFNumber
from ptext.io.tokenize.types.pdf_object import PDFObject


class ModifyTransformationMatrix(CanvasOperator):
    """
    Modify the current transformation matrix (CTM) by concatenating
    the specified matrix (see 8.3.2, "Coordinate Spaces"). Although the
    operands specify a matrix, they shall be written as six separate
    numbers, not as an array.
    """

    def __init__(self):
        super().__init__("cm", 6)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):
        for i in range(0, 6):
            if not isinstance(operands[i], PDFNumber):
                raise PDFTypeError(
                    expected_type=PDFNumber, received_type=operands[i].__class__
                )
        mtx = Matrix.matrix_from_six_values(
            operands[0].get_decimal_value(),
            operands[1].get_decimal_value(),
            operands[2].get_decimal_value(),
            operands[3].get_decimal_value(),
            operands[4].get_decimal_value(),
            operands[5].get_decimal_value(),
        )
        canvas.graphics_state.ctm = mtx.mul(canvas.graphics_state.ctm)
