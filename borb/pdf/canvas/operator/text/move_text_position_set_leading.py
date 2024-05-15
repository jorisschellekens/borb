#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Move to the start of the next line, offset from the start of the current line by
(tx , ty). As a side effect, this operator shall set the leading parameter in
the text state. This operator shall have the same effect as this code:
−ty TL
tx ty Td
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class MoveTextPositionSetLeading(CanvasOperator):
    """
    Move to the start of the next line, offset from the start of the current line by
    (tx , ty). As a side effect, this operator shall set the leading parameter in
    the text state. This operator shall have the same effect as this code:
    −ty TL
    tx ty Td
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("TD", 2)

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
        Invoke the TD operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        assert isinstance(operands[0], Decimal), "Operand 0 of TD must be a Decimal"
        assert isinstance(operands[1], Decimal), "Operand 1 of TD must be a Decimal"

        set_text_leading_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("TL")
        assert (
            set_text_leading_op
        ), "Operand TL must be defined for operator TD to function"
        set_text_leading_op.invoke(
            canvas_stream_processor, [bDecimal(-operands[1])], event_listeners
        )

        move_text_position_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("Td")
        assert (
            move_text_position_op
        ), "Operand Td must be defined for operator TD to function"
        move_text_position_op.invoke(canvas_stream_processor, operands, event_listeners)
