#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Same as RG but used for nonstroking operations.
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetRGBNonStroking(CanvasOperator):
    """
    Same as RG but used for nonstroking operations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("rg", 3)

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
        Invoke the rg operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        # fmt: off
        assert isinstance(operands[0], Decimal), "operand 0 of rg operator must be of type Decimal"
        assert isinstance(operands[1], Decimal), "operand 1 of rg operator must be of type Decimal"
        assert isinstance(operands[2], Decimal), "operand 2 of rg operator must be of type Decimal"
        # fmt: on

        # set non_stroke_color
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.non_stroke_color = RGBColor(
            operands[0], operands[1], operands[2]
        )
