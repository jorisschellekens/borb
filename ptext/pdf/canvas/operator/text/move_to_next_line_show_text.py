#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Move to the next line and show a text string. This operator shall have the
    same effect as the code
    T*
    string Tj
"""
import typing
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class MoveToNextLineShowText(CanvasOperator):
    """
    Move to the next line and show a text string. This operator shall have the
    same effect as the code
    T*
    string Tj
    """

    def __init__(self):
        super().__init__("'", 1)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the ' operator
        """
        move_to_next_line_op: typing.Optional[CanvasOperator] = canvas.get_operator(
            "T*"
        )
        assert move_to_next_line_op
        move_to_next_line_op.invoke(canvas, [])

        show_text_op: typing.Optional[CanvasOperator] = canvas.get_operator("Tj")
        assert show_text_op
        show_text_op.invoke(canvas, operands)
