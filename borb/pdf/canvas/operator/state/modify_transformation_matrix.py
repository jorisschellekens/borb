#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Modify the current transformation matrix (CTM) by concatenating
    the specified matrix (see 8.3.2, "Coordinate Spaces"). Although the
    operands specify a matrix, they shall be written as six separate
    numbers, not as an array.
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.geometry.matrix import Matrix
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class ModifyTransformationMatrix(CanvasOperator):
    """
    Modify the current transformation matrix (CTM) by concatenating
    the specified matrix (see 8.3.2, "Coordinate Spaces"). Although the
    operands specify a matrix, they shall be written as six separate
    numbers, not as an array.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("cm", 6)

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
        Invoke the cm operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        assert isinstance(operands[0], Decimal), "Operand 0 of cm must be a Decimal"
        assert isinstance(operands[1], Decimal), "Operand 1 of cm must be a Decimal"
        assert isinstance(operands[2], Decimal), "Operand 2 of cm must be a Decimal"
        assert isinstance(operands[3], Decimal), "Operand 3 of cm must be a Decimal"
        assert isinstance(operands[4], Decimal), "Operand 4 of cm must be a Decimal"
        assert isinstance(operands[5], Decimal), "Operand 5 of cm must be a Decimal"
        mtx = Matrix.matrix_from_six_values(
            operands[0],
            operands[1],
            operands[2],
            operands[3],
            operands[4],
            operands[5],
        )
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.ctm = mtx.mul(canvas.graphics_state.ctm)
