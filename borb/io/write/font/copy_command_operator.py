#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This CanvasOperator copies an existing operator and writes its bytes to a content stream of the canvas.
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.io.read.types import HexadecimalString
from borb.io.read.types import Name
from borb.io.read.types import String
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class CopyCommandOperator(CanvasOperator):
    """
    This CanvasOperator copies an existing operator and writes its bytes to a content stream of the canvas.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self, operator_to_copy: CanvasOperator, output_content_stream: bytearray
    ):
        super().__init__("", 0)
        self._operator_to_copy = operator_to_copy
        self._output_content_stream: bytearray = output_content_stream

    #
    # PRIVATE
    #

    def _operand_to_str(self, op: AnyPDFType) -> str:
        if isinstance(op, Decimal):
            return str(op)
        if isinstance(op, HexadecimalString):
            return "<" + str(op) + ">"
        if isinstance(op, String):
            return "(" + str(op) + ")"
        if isinstance(op, Name):
            return "/" + str(op)
        if isinstance(op, list):
            return "[" + "".join([self._operand_to_str(x) + " " for x in op])[:-1] + "]"
        return ""

    #
    # PUBLIC
    #

    def get_number_of_operands(self) -> int:
        """
        Return the number of operands for this CanvasOperator
        """
        return self._operator_to_copy.get_number_of_operands()

    def get_text(self) -> str:
        """
        Return the str that invokes this CanvasOperator
        """
        return self._operator_to_copy.get_text()

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore[name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore[name-defined]
    ) -> None:
        """
        Invokes this CanvasOperator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may need to be notified
        :return:                            None
        """

        # execute command
        self._operator_to_copy.invoke(canvas_stream_processor, operands)

        # copy command in content stream
        canvas = canvas_stream_processor.get_canvas()

        # copy operand string
        # fmt: off
        self._output_content_stream += b"\n"
        self._output_content_stream += b"".join([(bytes(self._operand_to_str(s), encoding="utf8") + b" ") for s in operands])
        self._output_content_stream += bytes(self.get_text(), encoding="utf8")
        # fmt: on
