import copy
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.geometry.matrix import Matrix
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFFloat, PDFNumber
from ptext.primitive.pdf_object import PDFObject


class SetTextMatrix(CanvasOperator):
    """
    Set the text matrix, Tm , and the text line matrix, Tlm :
    Tm = Tlm = [[a,b,0], [c,d,0],[e,f,1]]
    The operands shall all be numbers, and the initial value for Tm and Tlm
    shall be the identity matrix, [ 1 0 0 1 0 0 ]. Although the operands
    specify a matrix, they shall be passed to Tm as six separate numbers, not
    as an array.
    The matrix specified by the operands shall not be concatenated onto the
    current text matrix, but shall replace it.
    """

    def __init__(self):
        super().__init__("Tm", 6)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):

        for i in range(0, 6):
            if not isinstance(operands[i], PDFNumber):
                raise PDFTypeError(
                    expected_type=PDFNumber, received_type=operands[i].__class__
                )

        mtx = Matrix.matrix_from_six_values(
            operands[0].get_float_value(),
            operands[1].get_float_value(),
            operands[2].get_float_value(),
            operands[3].get_float_value(),
            operands[4].get_float_value(),
            operands[5].get_float_value(),
        )
        canvas.graphics_state.text_matrix = mtx
        canvas.graphics_state.text_line_matrix = copy.deepcopy(mtx)
