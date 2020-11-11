import copy
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.object.canvas.geometry.matrix import Matrix
from ptext.object.canvas.operator.canvas_operator import CanvasOperator
from ptext.primitive.pdf_number import PDFNumber
from ptext.primitive.pdf_object import PDFObject


class MoveTextPosition(CanvasOperator):
    """
    Move to the start of the next line, offset from the start of the current line by
    (tx , ty). t x and t y shall denote numbers expressed in unscaled text space
    units. More precisely, this operator shall perform these assignments:
    Tm = Tlm = [[1,0,0], [0,1,0],[tx,ty,1]] * Tlm
    """

    def __init__(self):
        super().__init__("Td", 2)

    def invoke(self, canvas: "Canvas", operands: List[PDFObject] = []):

        if not isinstance(operands[0], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[0].__class__
            )
        if not isinstance(operands[1], PDFNumber):
            raise PDFTypeError(
                expected_type=PDFNumber, received_type=operands[1].__class__
            )

        tx = operands[0].get_float_value()
        ty = operands[1].get_float_value()

        m = Matrix.identity_matrix()
        m[2][0] = tx
        m[2][1] = ty

        canvas.graphics_state.text_matrix = m.mul(
            canvas.graphics_state.text_line_matrix
        )
        canvas.graphics_state.text_line_matrix = copy.deepcopy(
            canvas.graphics_state.text_matrix
        )
