#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Show one or more text strings, allowing individual glyph positioning. Each
element of array shall be either a string or a number.
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class ShowTextWithGlyphPositioning(CanvasOperator):
    """
    Show one or more text strings, allowing individual glyph positioning. Each
    element of array shall be either a string or a number. If the element is a
    string, this operator shall show the string. If it is a number, the operator
    shall adjust the text position by that amount; that is, it shall translate the
    text matrix, T . The number shall be expressed in thousandths of a unit
    mof text space (see 9.4.4, "Text Space Details"). This amount shall be
    subtracted from the current horizontal or vertical coordinate, depending
    on the writing mode. In the default coordinate system, a positive
    adjustment has the effect of moving the next glyph painted either to the
    left or down by the given amount. Figure 46 shows an example of the
    effect of passing offsets to TJ.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("TJ", 1)

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
        Invoke the TJ operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """

        assert isinstance(operands[0], typing.List), "Operand 0 of TJ must be a List"
        canvas = canvas_stream_processor.get_canvas()

        # handle Font being a Name (optimization)
        assert canvas.graphics_state.font is not None
        font_name: typing.Optional[Name] = None
        if isinstance(canvas.graphics_state.font, Name):
            font_name = canvas.graphics_state.font
            canvas.graphics_state.font = canvas_stream_processor.get_resource(
                "Font", canvas.graphics_state.font
            )

        for i in range(0, len(operands[0])):
            obj = operands[0][i]

            # display string
            if isinstance(obj, String):
                assert isinstance(obj, String)
                tri = ChunkOfTextRenderEvent(canvas.graphics_state, obj)
                # render
                for l in event_listeners:
                    # noinspection PyProtectedMember
                    l._event_occurred(tri)
                # update text rendering location
                canvas.graphics_state.text_matrix[2][0] += tri.get_baseline().width
                continue

            # adjust
            if isinstance(obj, Decimal):
                assert isinstance(obj, Decimal)
                gs = canvas.graphics_state
                adjust_unscaled = obj
                adjust_scaled = (
                    -adjust_unscaled
                    * Decimal(0.001)
                    * gs.font_size
                    * (gs.horizontal_scaling / 100)
                )
                gs.text_matrix[2][0] -= adjust_scaled

        # restore
        if font_name is not None:
            canvas.graphics_state.font = font_name
