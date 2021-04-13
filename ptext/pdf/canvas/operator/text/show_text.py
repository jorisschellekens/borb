#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Show a text string.
"""
from typing import List

from ptext.io.read.types import AnyPDFType, String
from ptext.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class ShowText(CanvasOperator):
    """
    Show a text string.
    """

    def __init__(self):
        super().__init__("Tj", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the Tj operator
        """
        assert isinstance(operands[0], String)
        tri = ChunkOfTextRenderEvent(canvas.graphics_state, operands[0])
        # render
        canvas._event_occurred(tri)
        # update text rendering location
        canvas.graphics_state.text_matrix[2][0] += tri.get_baseline().width
