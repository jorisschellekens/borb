#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'ri' operator: Set the color rendering intent in the graphics state.

This operator specifies the color rendering intent to be used in the graphics state.
The rendering intent controls how colors are mapped in the output device, and it
helps manage color discrepancies between different color spaces (such as from RGB to
CMYK or vice versa).

The operand for this operator is a name object that identifies the rendering intent.
Common rendering intents include "Perceptual", "RelativeColorimetric", "Saturation",
and "AbsoluteColorimetric", which define different ways of handling color conversions.

Note:
    The rendering intent can affect how color values are processed, especially when
    printing or displaying content across devices with varying color gamuts. This operator
    should be used in conjunction with color management settings for consistent color output.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorri(Operator):
    """
    The 'ri' operator: Set the color rendering intent in the graphics state.

    This operator specifies the color rendering intent to be used in the graphics state.
    The rendering intent controls how colors are mapped in the output device, and it
    helps manage color discrepancies between different color spaces (such as from RGB to
    CMYK or vice versa).

    The operand for this operator is a name object that identifies the rendering intent.
    Common rendering intents include "Perceptual", "RelativeColorimetric", "Saturation",
    and "AbsoluteColorimetric", which define different ways of handling color conversions.

    Note:
        The rendering intent can affect how color values are processed, especially when
        printing or displaying content across devices with varying color gamuts. This operator
        should be used in conjunction with color management settings for consistent color output.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def apply(
        self,
        operands: typing.List[PDFType],
        page: Page,
        source: Source,
    ) -> None:
        """
        Apply the operator's logic to the given `Page`.

        This method executes the operator using the provided operands, applying its
        effects to the specified `Page` via the `Source` processor. Subclasses should
        override this method to implement specific operator behavior.

        :param page: The `Page` object to which the operator is applied.
        :param source: The `Source` object managing the content stream.
        :param operands: A list of `PDFType` objects representing the operator's operands.
        """
        assert isinstance(operands[0], name)
        source.color_rendering_intent = operands[0]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "ri"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
