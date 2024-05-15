#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(PDF 1.2) Same as SC but also supports Pattern, Separation, DeviceN
and ICCBased colour spaces.
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.color.color import CMYKColor
from borb.pdf.canvas.color.color import GrayColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.color.color import Separation
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetColorStroking(CanvasOperator):
    """
    (PDF 1.2) Same as SC but also supports Pattern, Separation, DeviceN
    and ICCBased colour spaces.
    If the current stroking colour space is a Separation, DeviceN, or
    ICCBased colour space, the operands c 1 ... c n shall be numbers. The
    number of operands and their interpretation depends on the colour space.
    If the current stroking colour space is a Pattern colour space, name shall
    be the name of an entry in the Pattern subdictionary of the current
    resource dictionary (see 7.8.3, "Resource Dictionaries"). For an
    uncoloured tiling pattern (PatternType = 1 and PaintType = 2), c 1 ... c n
    shall be component values specifying a colour in the pattern’s underlying
    colour space. For other types of patterns, these operands shall not be
    specified.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, canvas_stream_processor: "CanvasStreamProcessor"):
        super().__init__("SCN", 0)
        self._canvas = canvas_stream_processor.get_canvas()

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_number_of_operands(self) -> int:
        """
        This function returns the number of operands for the SCN operator.
        The number of operands and their interpretation depends on the colour space.
        :return:    the number of operands
        """
        stroke_color_space = self._canvas.graphics_state.stroke_color_space
        if stroke_color_space == "DeviceCMYK":
            return 4
        if stroke_color_space == "DeviceGray":
            return 1
        if stroke_color_space == "DeviceRGB":
            return 3
        # separation
        if (
            isinstance(stroke_color_space, typing.List)
            and len(stroke_color_space) == 4
            and stroke_color_space[0] == "Separation"
        ):
            return 1
        return self._number_of_operands

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the SCN operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        canvas = canvas_stream_processor.get_canvas()
        stroke_color_space = canvas.graphics_state.stroke_color_space
        if stroke_color_space == "DeviceCMYK":
            assert isinstance(
                operands[0], Decimal
            ), "Operand 0 of SCN must be a Decimal"
            assert isinstance(
                operands[1], Decimal
            ), "Operand 1 of SCN must be a Decimal"
            assert isinstance(
                operands[2], Decimal
            ), "Operand 2 of SCN must be a Decimal"
            assert isinstance(
                operands[3], Decimal
            ), "Operand 3 of SCN must be a Decimal"
            canvas.graphics_state.stroke_color = CMYKColor(
                operands[0],
                operands[1],
                operands[2],
                operands[3],
            )
            return

        if stroke_color_space == "DeviceGray":
            assert isinstance(
                operands[0], Decimal
            ), "Operand 0 of SCN must be a Decimal"
            canvas.graphics_state.stroke_color = GrayColor(operands[0])
            return

        if stroke_color_space == "DeviceRGB":
            assert isinstance(
                operands[0], Decimal
            ), "Operand 0 of SCN must be a Decimal"
            assert isinstance(
                operands[1], Decimal
            ), "Operand 1 of SCN must be a Decimal"
            assert isinstance(
                operands[2], Decimal
            ), "Operand 2 of SCN must be a Decimal"
            canvas.graphics_state.stroke_color = RGBColor(
                operands[0],
                operands[1],
                operands[2],
            )
            return

        # separation
        if (
            isinstance(stroke_color_space, typing.List)
            and stroke_color_space[0] == "Separation"
        ):
            assert isinstance(
                operands[0], Decimal
            ), "Operand 0 of SCN must be a Decimal"
            canvas.graphics_state.stroke_color = Separation(
                canvas.graphics_state.stroke_color_space, [operands[0]]
            )
            return
