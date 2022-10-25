#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set the text rendering mode, T mode , to render, which shall be an integer.
Initial value: 0.
"""

import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetTextRenderingMode(CanvasOperator):
    """
    Set the text rendering mode, T mode , to render, which shall be an integer.
    Initial value: 0.
    """

    def __init__(self):
        super().__init__("Tr", 1)

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the Tr operator
        """
        # TODO
        pass
