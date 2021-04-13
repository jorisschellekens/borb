#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Stroke the path.
"""
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.event.line_render_event import LineRenderEvent
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class StrokePath(CanvasOperator):
    """
    Stroke the path.
    """

    def __init__(self):
        super().__init__("S", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the S operator
        """

        # get graphic state
        gs = canvas.graphics_state

        # notify listeners
        for l in gs.path:
            canvas._event_occurred(LineRenderEvent(gs, l))

        # clear path
        gs.path = []
