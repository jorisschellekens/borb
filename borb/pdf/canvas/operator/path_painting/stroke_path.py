#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stroke the path.
"""
from typing import List

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.event.line_render_event import LineRenderEvent
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class StrokePath(CanvasOperator):
    """
    Stroke the path.
    """

    def __init__(self):
        super().__init__("S", 0)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],
    ) -> None:  # type: ignore [name-defined]
        """
        Invoke the S operator
        """

        # get graphic state
        canvas = canvas_stream_processor.get_canvas()
        gs = canvas.graphics_state

        # notify listeners
        for el in event_listeners:
            for l in gs.path:
                el._event_occurred(LineRenderEvent(gs, l))

        # clear path
        gs.path = []
