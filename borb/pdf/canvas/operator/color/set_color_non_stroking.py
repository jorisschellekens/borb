#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(PDF 1.2) Same as SCN but used for nonstroking operations.
"""
import typing
from decimal import Decimal

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.color.color import CMYKColor
from borb.pdf.canvas.color.color import GrayColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.color.color import Separation
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetColorNonStroking(CanvasOperator):
    """
    (PDF 1.2) Same as SCN but used for nonstroking operations.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, canvas_stream_processor: "CanvasStreamProcessor"):
        super().__init__("scn", 0)
        self._canvas = canvas_stream_processor.get_canvas()

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_number_of_operands(self) -> int:
        """
        This function returns the number of operands for the scn operator.
        The number of operands and their interpretation depends on the colour space.
        """
        non_stroke_color_space = self._canvas.graphics_state.non_stroke_color_space
        if non_stroke_color_space == "DeviceCMYK":
            return 4
        if non_stroke_color_space == "DeviceGray":
            return 1
        if non_stroke_color_space == "DeviceRGB":
            return 3
        # separation
        if (
            isinstance(non_stroke_color_space, typing.List)
            and len(non_stroke_color_space) == 4
            and non_stroke_color_space[0] == "Separation"
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
        Invoke the scn operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        canvas = canvas_stream_processor.get_canvas()
        non_stroke_color_space = canvas.graphics_state.non_stroke_color_space
        if non_stroke_color_space == "DeviceCMYK":
            # fmt: off
            assert isinstance(operands[0], Decimal), "Operand 0 of scn must be a Decimal"
            assert isinstance(operands[1], Decimal), "Operand 1 of scn must be a Decimal"
            assert isinstance(operands[2], Decimal), "Operand 2 of scn must be a Decimal"
            assert isinstance(operands[3], Decimal), "Operand 3 of scn must be a Decimal"
            canvas.graphics_state.non_stroke_color = CMYKColor(
                operands[0],
                operands[1],
                operands[2],
                operands[3],
            )
            return
            # fmt: on

        if non_stroke_color_space == "DeviceGray":
            # fmt: off
            assert isinstance(operands[0], Decimal), "Operand 0 of scn must be a Decimal"
            canvas.graphics_state.non_stroke_color = GrayColor(operands[0])
            return
            # fmt: on

        if non_stroke_color_space == "DeviceRGB":
            # fmt: off
            assert isinstance(operands[0], Decimal), "Operand 0 of scn must be a Decimal"
            assert isinstance(operands[1], Decimal), "Operand 1 of scn must be a Decimal"
            assert isinstance(operands[2], Decimal), "Operand 2 of scn must be a Decimal"
            canvas.graphics_state.non_stroke_color = RGBColor(
                operands[0],
                operands[1],
                operands[2],
            )
            return
            # fmt: on

        # separation
        if (
            isinstance(non_stroke_color_space, typing.List)
            and non_stroke_color_space[0] == "Separation"
        ):
            # fmt: off
            assert isinstance(operands[0], Decimal), "Operand 0 of scn must be a Decimal"
            canvas.graphics_state.non_stroke_color = Separation(canvas.graphics_state.non_stroke_color_space, [operands[0]])
            return
            # fmt: on
