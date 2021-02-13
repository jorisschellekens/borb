from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetLineWidth(CanvasOperator):
    """
    Set the line width in the graphics state (see 8.4.3.2, "Line Width").
    """

    def __init__(self):
        super().__init__("w", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the w operator
        """
        assert isinstance(operands[0], Decimal)
        canvas.graphics_state.line_width = operands[0]
