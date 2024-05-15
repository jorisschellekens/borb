#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Move to the next line and show a text string. This operator shall have the
same effect as the code
T*
string Tj
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class MoveToNextLineShowText(CanvasOperator):
    """
    Move to the next line and show a text string. This operator shall have the
    same effect as the code
    T*
    string Tj
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("'", 1)

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
        Invoke the ' operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        move_to_next_line_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("T*")
        assert (
            move_to_next_line_op
        ), "Operator T* must be defined for operator ' to function."
        move_to_next_line_op.invoke(canvas_stream_processor, [], event_listeners)

        show_text_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("Tj")
        assert show_text_op, "Operator Tj must be defined for operator ' to function"
        show_text_op.invoke(canvas_stream_processor, operands, event_listeners)
