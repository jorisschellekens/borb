import copy
from typing import List

from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class PushGraphicsState(CanvasOperator):
    """
    Save the current graphics state on the graphics state stack (see
    8.4.2, "Graphics State Stack").
    """

    def __init__(self):
        super().__init__("q", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        canvas.graphics_state_stack.append(copy.deepcopy(canvas.graphics_state))
