#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    End a text object, discarding the text matrix.
"""
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.event.end_text_event import EndTextEvent
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class EndTextObject(CanvasOperator):
    """
    End a text object, discarding the text matrix.
    """

    def __init__(self):
        super().__init__("ET", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):  # type: ignore [name-defined]
        """
        Invoke the ET operator
        """
        canvas.graphics_state.text_matrix = None
        canvas.graphics_state.text_line_matrix = None
        canvas.event_occurred(EndTextEvent())
