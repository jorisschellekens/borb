#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Move to the start of the next line, offset from the start of the current line by
(tx , ty). t x and t y shall denote numbers expressed in unscaled text space
units. More precisely, this operator shall perform these assignments:
Tm = Tlm = [[1,0,0], [0,1,0],[tx,ty,1]] * Tlm
"""
import copy
from decimal import Decimal
from typing import List

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.geometry.matrix import Matrix
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class MoveTextPosition(CanvasOperator):
    """
    Move to the start of the next line, offset from the start of the current line by
    (tx , ty). t x and t y shall denote numbers expressed in unscaled text space
    units. More precisely, this operator shall perform these assignments:
    Tm = Tlm = [[1,0,0], [0,1,0],[tx,ty,1]] * Tlm
    """

    def __init__(self):
        super().__init__("Td", 2)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],
    ) -> None:  # type: ignore [name-defined]
        """
        Invoke the Td operator
        """
        assert isinstance(operands[0], Decimal), "Operand 0 of Td must be a Decimal"
        assert isinstance(operands[1], Decimal), "Operand 1 of Td must be a Decimal"

        tx = operands[0]
        ty = operands[1]

        m = Matrix.identity_matrix()
        m[2][0] = tx
        m[2][1] = ty

        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.text_matrix = m.mul(
            canvas.graphics_state.text_line_matrix
        )
        canvas.graphics_state.text_line_matrix = copy.deepcopy(
            canvas.graphics_state.text_matrix
        )
