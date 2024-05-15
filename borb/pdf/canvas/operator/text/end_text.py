#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
End a text object, discarding the text matrix.
"""

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.event.end_text_event import EndTextEvent
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class EndTextObject(CanvasOperator):
    """
    End a text object, discarding the text matrix.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("ET", 0)

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
        Invoke the ET operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.text_matrix = None
        canvas.graphics_state.text_line_matrix = None
        for l in event_listeners:
            # noinspection PyProtectedMember
            l._event_occurred(EndTextEvent())
