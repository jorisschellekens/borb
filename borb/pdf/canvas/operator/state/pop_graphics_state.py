#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Restore the graphics state by removing the most recently saved
state from the stack and making it the current state (see 8.4.2,
"Graphics State Stack").
"""

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class PopGraphicsState(CanvasOperator):
    """
    Restore the graphics state by removing the most recently saved
    state from the stack and making it the current state (see 8.4.2,
    "Graphics State Stack").
    """

    def __init__(self):
        super().__init__("Q", 0)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the Q operator
        """
        canvas = canvas_stream_processor.get_canvas()
        assert (
            len(canvas.graphics_state_stack) > 0
        ), "Stack underflow. Q operator was applied to an empty stack."
        canvas.graphics_state = canvas.graphics_state_stack.pop(-1)
