#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
End a text object, discarding the text matrix.
"""
from typing import List

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.event.end_text_event import EndTextEvent
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class EndTextObject(CanvasOperator):
    """
    End a text object, discarding the text matrix.
    """

    def __init__(self):
        super().__init__("ET", 0)

    def invoke(self, canvas_stream_processor: "CanvasStreamProcessor", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the ET operator
        """
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.text_matrix = None
        canvas.graphics_state.text_line_matrix = None
        canvas._event_occurred(EndTextEvent())
