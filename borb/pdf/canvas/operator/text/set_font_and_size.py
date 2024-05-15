#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set the text font, T f , to font and the text font size, T fs , to size. font shall be
the name of a font resource in the Font subdictionary of the current
resource dictionary; size shall be a number representing a scale factor.
There is no initial value for either font or size; they shall be specified
explicitly by using Tf before any text is shown.
"""

import typing

from borb.io.read.types import AnyPDFType
from borb.io.read.types import Decimal as bDecimal
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetFontAndSize(CanvasOperator):
    """
    Set the text font, T f , to font and the text font size, T fs , to size. font shall be
    the name of a font resource in the Font subdictionary of the current
    resource dictionary; size shall be a number representing a scale factor.
    There is no initial value for either font or size; they shall be specified
    explicitly by using Tf before any text is shown.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__("Tf", 2)

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
        Invoke the Tf operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """

        # lookup font dictionary
        font_ref = canvas_stream_processor.get_resource("Font", operands[0])
        assert font_ref is not None
        assert isinstance(font_ref, Font)

        # font size
        font_size = operands[1]
        assert isinstance(font_size, bDecimal)

        # set state
        canvas = canvas_stream_processor.get_canvas()
        canvas.graphics_state.font_size = font_size
        canvas.graphics_state.font = operands[
            0
        ]  # in stead of setting the Font in the graphics_state, we explictly set the Name of the Font. This is a lot cheaper to copy by the Q/q operator.
