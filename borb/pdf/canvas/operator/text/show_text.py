#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Show a text string.
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class ShowText(CanvasOperator):
    """
    Show a text string.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("Tj", 1)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the Tj operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
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
            # noinspection PyProtectedMember
            l._event_occurred(tri)

        # update text rendering location
        canvas.graphics_state.text_matrix[2][0] += tri.get_baseline().width

        # restore
        if font_name is not None:
            canvas.graphics_state.font = font_name
