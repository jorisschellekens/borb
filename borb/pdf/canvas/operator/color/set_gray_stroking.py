#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set the stroking colour space to DeviceGray (or the DefaultGray colour
space; see 8.6.5.6, "Default Colour Spaces") and set the gray level to use
for stroking operations. gray shall be a number between 0.0 (black) and
1.0 (white).
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.color.color import GrayColor
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetGrayStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceGray (or the DefaultGray colour
    space; see 8.6.5.6, "Default Colour Spaces") and set the gray level to use
    for stroking operations. gray shall be a number between 0.0 (black) and
    1.0 (white).
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("G", 1)

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
        Invoke the G operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        assert isinstance(operands[0], Decimal), "Operand 0 of G must be a Decimal"
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.stroke_color = GrayColor(operands[0])
