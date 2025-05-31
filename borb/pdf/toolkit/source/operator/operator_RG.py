#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'RG' operator: Set the stroking color space to DeviceRGB and set the color for stroking operations.

This operator sets the current stroking color space to DeviceRGB (or the DefaultRGB color space),
and defines the color to be used for stroking operations. The operands specify the red, green,
and blue components of the color, each as a number between 0.0 (minimum intensity) and 1.0
(maximum intensity).

The color components (red, green, and blue) are applied to the current graphics state and used
when stroking paths. If the color space is set to DeviceRGB, the operands represent the RGB values
for the stroking color.

This operator is important for controlling the appearance of paths, lines, and other graphic elements
in a PDF document, especially when creating colored outlines or borders.

Note:
    The RG operator affects only the stroking color. To set the color for filling paths, use the
    'rg' operator for nonstroking operations.
"""
import typing

from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorRG(Operator):
    """
    The 'RG' operator: Set the stroking color space to DeviceRGB and set the color for stroking operations.

    This operator sets the current stroking color space to DeviceRGB (or the DefaultRGB color space),
    and defines the color to be used for stroking operations. The operands specify the red, green,
    and blue components of the color, each as a number between 0.0 (minimum intensity) and 1.0
    (maximum intensity).

    The color components (red, green, and blue) are applied to the current graphics state and used
    when stroking paths. If the color space is set to DeviceRGB, the operands represent the RGB values
    for the stroking color.

    This operator is important for controlling the appearance of paths, lines, and other graphic elements
    in a PDF document, especially when creating colored outlines or borders.

    Note:
        The RG operator affects only the stroking color. To set the color for filling paths, use the
        'rg' operator for nonstroking operations.
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
        source.stroke_color_space = name("DeviceRGB")
        source.stroke_color = RGBColor(
            red=int(red * 255), green=int(green * 255), blue=int(blue * 255)
        )
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "RG"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 3
