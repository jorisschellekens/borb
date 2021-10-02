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
from decimal import Decimal

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
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the s operator
        """
        x: Decimal = operands[0]
        y: Decimal = operands[1]
        width: Decimal = operands[2]
        height: Decimal = operands[3]

        moveto_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("m")
        moveto_op.invoke(canvas_stream_processor, [x, y], event_listeners)

        line_to_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("l")
        line_to_op.invoke(canvas_stream_processor, [x + width, y], event_listeners)
        line_to_op.invoke(
            canvas_stream_processor, [x + width, y + height], event_listeners
        )
        line_to_op.invoke(canvas_stream_processor, [x, y + height], event_listeners)

        close_subpath_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("h")
        close_subpath_op.invoke(canvas_stream_processor, [], event_listeners)
