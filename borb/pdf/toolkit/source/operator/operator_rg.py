#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'rg' operator: Set the nonstroking color using the DeviceRGB color space.

This operator sets the nonstroking color in the graphics state by specifying
a color using the DeviceRGB color space (or the DefaultRGB color space, as defined
in the PDF specification). The color is defined by three operands, each representing
a component of the color: red, green, and blue. Each component is a number between
0.0 (minimum intensity) and 1.0 (maximum intensity).

This operator is functionally equivalent to 'RG', but it is used specifically
for nonstroking operations (such as filling or text rendering).

Note:
    The values provided for red, green, and blue should be in the range [0.0, 1.0].
    A color with values [0.0, 0.0, 0.0] corresponds to black, and [1.0, 1.0, 1.0]
    corresponds to white.
"""
import typing

from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorrg(Operator):
    """
    The 'rg' operator: Set the nonstroking color using the DeviceRGB color space.

    This operator sets the nonstroking color in the graphics state by specifying
    a color using the DeviceRGB color space (or the DefaultRGB color space, as defined
    in the PDF specification). The color is defined by three operands, each representing
    a component of the color: red, green, and blue. Each component is a number between
    0.0 (minimum intensity) and 1.0 (maximum intensity).

    This operator is functionally equivalent to 'RG', but it is used specifically
    for nonstroking operations (such as filling or text rendering).

    Note:
        The values provided for red, green, and blue should be in the range [0.0, 1.0].
        A color with values [0.0, 0.0, 0.0] corresponds to black, and [1.0, 1.0, 1.0]
        corresponds to white.
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
        assert isinstance(operands[0], float) or isinstance(operands[0], int)
        assert isinstance(operands[1], float) or isinstance(operands[1], int)
        assert isinstance(operands[2], float) or isinstance(operands[2], int)
        red: typing.Union[float, int] = operands[0]
        green: typing.Union[float, int] = operands[1]
        blue: typing.Union[float, int] = operands[2]
        source.non_stroke_color_space = name("DeviceRGB")
        source.non_stroke_color = RGBColor(
            red=int(red * 255),
            green=int(green * 255),
            blue=int(blue * 255),
        )
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "rg"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 3
