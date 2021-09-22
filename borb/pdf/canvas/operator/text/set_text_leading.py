#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set the text leading, T l , to leading, which shall be a number expressed in
unscaled text space units. Text leading shall be used only by the T*, ', and
" operators. Initial value: 0.
"""
from decimal import Decimal
from typing import List

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextLeading(CanvasOperator):
    """
    Set the text leading, T l , to leading, which shall be a number expressed in
    unscaled text space units. Text leading shall be used only by the T*, ', and
    " operators. Initial value: 0.
    """

    def __init__(self):
        super().__init__("TL", 1)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],
    ) -> None:  # type: ignore [name-defined]
        """
        Invoke the TL operator
        """
        assert isinstance(operands[0], Decimal)
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.leading = operands[0]
