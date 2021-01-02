from typing import List

from ptext.io.read_transform.types import AnyPDFType, Name
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class BeginMarkedContent(CanvasOperator):
    """
    Begin a marked-content sequence terminated by a balancing EMC
    operator. tag shall be a name object indicating the role or significance of
    the sequence.
    """

    def __init__(self):
        super().__init__("BMC", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        assert isinstance(operands[0], Name)
        canvas.marked_content_stack.append(operands[0])
