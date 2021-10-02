#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An operator in a programming language is a symbol that tells the compiler or interpreter to perform specific mathematical,
relational or logical operation and produce final result.
CanvasOperator defines an interface to work on Canvas objects. Typically these operators involve drawing graphics, text,
setting the active color and so on
"""
import typing

from borb.io.read.types import AnyPDFType


class CanvasOperator:
    """
    An operator in a programming language is a symbol that tells the compiler or interpreter to perform specific mathematical,
    relational or logical operation and produce final result.
    CanvasOperator defines an interface to work on Canvas objects. Typically these operators involve drawing graphics, text,
    setting the active color and so on
    """

    def __init__(self, text: str, number_of_operands: int):
        self._text: str = text
        self._number_of_operands: int = number_of_operands

    def get_text(self) -> str:
        """
        Return the str that invokes this CanvasOperator
        """
        return self._text

    def get_number_of_operands(self) -> int:
        """
        Return the number of operands for this CanvasOperator
        """
        return self._number_of_operands

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invokes this CanvasOperator
        """
        pass
