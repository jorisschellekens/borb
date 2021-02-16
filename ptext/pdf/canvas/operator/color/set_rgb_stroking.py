#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Set the stroking colour space to DeviceRGB (or the DefaultRGB colour
    space; see 8.6.5.6, "Default Colour Spaces") and set the colour to use for
    stroking operations. Each operand shall be a number between 0.0
    (minimum intensity) and 1.0 (maximum intensity).
"""
from decimal import Decimal
from typing import List

from ptext.io.read.types import AnyPDFType
from ptext.pdf.canvas.color.color import RGBColor
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetRGBStroking(CanvasOperator):
    """
    Set the stroking colour space to DeviceRGB (or the DefaultRGB colour
    space; see 8.6.5.6, "Default Colour Spaces") and set the colour to use for
    stroking operations. Each operand shall be a number between 0.0
    (minimum intensity) and 1.0 (maximum intensity).
    """

    def __init__(self):
        super().__init__("RG", 3)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []) -> None:  # type: ignore [name-defined]
        """
        Invoke the RG operator
        """
        assert isinstance(operands[0], Decimal)
        assert isinstance(operands[1], Decimal)
        assert isinstance(operands[2], Decimal)
        r = operands[0]
        g = operands[1]
        b = operands[2]
        canvas.graphics_state.stroke_color = RGBColor(r, g, b)
