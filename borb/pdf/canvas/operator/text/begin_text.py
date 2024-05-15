#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Begin a text object, initializing the text matrix, Tm , and the text line matrix,
Tlm , to the identity matrix. Text objects shall not be nested; a second BT shall
not appear before an ET.
"""

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.event.begin_text_event import BeginTextEvent
from borb.pdf.canvas.geometry.matrix import Matrix
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class BeginTextObject(CanvasOperator):
    """
    Begin a text object, initializing the text matrix, Tm , and the text line matrix,
    Tlm , to the identity matrix. Text objects shall not be nested; a second BT shall
    not appear before an ET.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("BT", 0)

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
        Invoke the BT operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.text_matrix = Matrix.identity_matrix()
        canvas.graphics_state.text_line_matrix = Matrix.identity_matrix()
        for l in event_listeners:
            # noinspection PyProtectedMember
            l._event_occurred(BeginTextEvent())
