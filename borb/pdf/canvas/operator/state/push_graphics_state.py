#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Save the current graphics state on the graphics state stack (see
8.4.2, "Graphics State Stack").
"""
import copy
import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class PushGraphicsState(CanvasOperator):
    """
    Save the current graphics state on the graphics state stack (see
    8.4.2, "Graphics State Stack").
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("q", 0)

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
        Invoke the q operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state_stack.append(copy.deepcopy(canvas.graphics_state))
