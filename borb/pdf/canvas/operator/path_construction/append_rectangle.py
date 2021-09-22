#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Append a rectangle to the current path as a complete
subpath, with lower-left corner (x, y) and dimensions width
and height in user space. The operation
x y width height re
is equivalent to
x y m
( x + width ) y l
( x + width ) ( y + height ) l
x ( y + height ) l
h
"""
import typing
from typing import List

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class AppendRectangle(CanvasOperator):
    """
    Append a rectangle to the current path as a complete
    subpath, with lower-left corner (x, y) and dimensions width
    and height in user space. The operation
    x y width height re
    is equivalent to
    x y m
    ( x + width ) y l
    ( x + width ) ( y + height ) l
    x ( y + height ) l
    h
    """

    def __init__(self):
        super().__init__("s", 0)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],
    ) -> None:  # type: ignore [name-defined]
        """
        Invoke the s operator
        """
        moveto_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("m")
        line_to_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("l")
        close_subpath_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("h")

        # TODO
