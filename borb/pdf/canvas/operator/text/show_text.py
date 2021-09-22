#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Show a text string.
"""
import typing
from typing import List

from borb.io.read.types import AnyPDFType, Name, String
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class ShowText(CanvasOperator):
    """
    Show a text string.
    """

    def __init__(self):
        super().__init__("Tj", 1)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],
    ) -> None:  # type: ignore [name-defined]
        """
        Invoke the Tj operator
        """
        assert isinstance(operands[0], String), "Operand 0 of Tj must be a String"
        canvas = canvas_stream_processor.get_canvas()

        # handle Font being a Name (optimization)
        assert canvas.graphics_state.font is not None
        font_name: typing.Optional[Name] = None
        if isinstance(canvas.graphics_state.font, Name):
            font_name = canvas.graphics_state.font
            canvas.graphics_state.font = canvas_stream_processor.get_resource(
                "Font", canvas.graphics_state.font
            )

        tri = ChunkOfTextRenderEvent(canvas.graphics_state, operands[0])

        # render
        for l in event_listeners:
            l._event_occurred(tri)

        # update text rendering location
        canvas.graphics_state.text_matrix[2][0] += tri.get_baseline().width

        # restore
        if font_name is not None:
            canvas.graphics_state.font = font_name
