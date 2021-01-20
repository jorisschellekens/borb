from typing import List

from ptext.functionality.structure.line.line_render_event import LineRenderEvent
from ptext.io.read_transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class StrokePath(CanvasOperator):
    """
    Stroke the path.
    """

    def __init__(self):
        super().__init__("S", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]

        # get graphic state
        gs = canvas.graphics_state

        # notify listeners
        for l in gs.path:
            canvas.event_occurred(LineRenderEvent(l))

        # clear path
        gs.path = []
