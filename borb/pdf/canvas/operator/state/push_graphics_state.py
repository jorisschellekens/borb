#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Save the current graphics state on the graphics state stack (see
8.4.2, "Graphics State Stack").
"""
import copy
from typing import List

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class PushGraphicsState(CanvasOperator):
    """
    Save the current graphics state on the graphics state stack (see
    8.4.2, "Graphics State Stack").
    """

    def __init__(self):
        super().__init__("q", 0)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],
    ) -> None:  # type: ignore [name-defined]
        """
        Invoke the q operator
        """
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state_stack.append(copy.deepcopy(canvas.graphics_state))
