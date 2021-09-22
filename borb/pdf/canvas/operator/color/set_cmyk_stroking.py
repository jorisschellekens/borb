#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set the stroking colour space to DeviceCMYK (or the DefaultCMYK
colour space; see 8.6.5.6, "Default Colour Spaces") and set the colour to
use for stroking operations. Each operand shall be a number between 0.0
(zero concentration) and 1.0 (maximum concentration). The behaviour of
this operator is affected by the overprint mode (see 8.6.7, "Overprint
Control").
"""
from decimal import Decimal
from typing import List

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.color.color import CMYKColor
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetCMYKStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceCMYK (or the DefaultCMYK
    colour space; see 8.6.5.6, "Default Colour Spaces") and set the colour to
    use for stroking operations. Each operand shall be a number between 0.0
    (zero concentration) and 1.0 (maximum concentration). The behaviour of
    this operator is affected by the overprint mode (see 8.6.7, "Overprint
    Control").
    """

    def __init__(self):
        super().__init__("K", 4)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],
    ) -> None:  # type: ignore [name-defined]
        """
        Invoke the K operator
        """
        # fmt: off
        assert isinstance(operands[0], Decimal), "operand 0 of K operator must be of type Decimal"
        assert isinstance(operands[1], Decimal), "operand 1 of K operator must be of type Decimal"
        assert isinstance(operands[2], Decimal), "operand 2 of K operator must be of type Decimal"
        assert isinstance(operands[3], Decimal), "operand 3 of K operator must be of type Decimal"
        # fmt: on
        c = operands[0]
        m = operands[1]
        y = operands[2]
        k = operands[3]
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.stroke_color = CMYKColor(c, m, y, k)
