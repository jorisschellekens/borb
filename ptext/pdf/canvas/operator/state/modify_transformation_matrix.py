from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.geometry.matrix import Matrix
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class ModifyTransformationMatrix(CanvasOperator):
    """
    Modify the current transformation matrix (CTM) by concatenating
    the specified matrix (see 8.3.2, "Coordinate Spaces"). Although the
    operands specify a matrix, they shall be written as six separate
    numbers, not as an array.
    """

    def __init__(self):
        super().__init__("cm", 6)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        assert isinstance(operands[3], Decimal)
        assert isinstance(operands[4], Decimal)
        assert isinstance(operands[5], Decimal)
        mtx = Matrix.matrix_from_six_values(
            operands[0],
            operands[1],
            operands[2],
            operands[3],
            operands[4],
            operands[5],
        )
        canvas.graphics_state.ctm = mtx.mul(canvas.graphics_state.ctm)
