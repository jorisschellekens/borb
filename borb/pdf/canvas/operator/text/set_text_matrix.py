#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set the text matrix, Tm , and the text line matrix, Tlm :
Tm = Tlm = [[a,b,0], [c,d,0],[e,f,1]]
"""
import copy
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.geometry.matrix import Matrix
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextMatrix(CanvasOperator):
    """
    Set the text matrix, Tm , and the text line matrix, Tlm :
    Tm = Tlm = [[a,b,0], [c,d,0],[e,f,1]]

    The operands shall all be numbers, and the initial value for Tm and Tlm
    shall be the identity matrix, [ 1 0 0 1 0 0 ]. Although the operands
    specify a matrix, they shall be passed to Tm as six separate numbers, not
    as an array.

    The matrix specified by the operands shall not be concatenated onto the
    current text matrix, but shall replace it.
    """

    def __init__(self):
        super().__init__("Tm", 6)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the Tm operator
        """

        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        assert isinstance(operands[3], Decimal)
        assert isinstance(operands[4], Decimal)
        assert isinstance(operands[5], Decimal)

        mtx = Matrix.matrix_from_six_values(
            operands[0],
            operands[1],
            operands[2],
            operands[3],
            operands[4],
            operands[5],
        )
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.text_matrix = mtx
        canvas.graphics_state.text_line_matrix = copy.deepcopy(mtx)
