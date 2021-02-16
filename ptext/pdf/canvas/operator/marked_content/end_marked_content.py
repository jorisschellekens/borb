#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    End a marked-content sequence begun by a BMC or BDC operator.
"""
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class EndMarkedContent(CanvasOperator):
    """
    End a marked-content sequence begun by a BMC or BDC operator.
    """

    def __init__(self):
        super().__init__("EMC", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the EMC operator
        """
        assert len(canvas.marked_content_stack) > 0
        canvas.marked_content_stack.pop(-1)
