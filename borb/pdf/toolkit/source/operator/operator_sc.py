#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'sc' operator: Set the stroke color using the current color space.

The 'sc' operator is used in a PDF content stream to set the stroke color for subsequent
path operations. The color is specified using the current color space, which could be
either a device-dependent color space (e.g., RGB or CMYK) or a device-independent color
space (e.g., CIE-based color spaces). The 'sc' operator applies to the stroke color,
which is used when paths are stroked with the 'S' operator or similar.

The color values provided are based on the current color space in effect, and the operator
expects the correct number of parameters based on the type of color space (e.g., 1 for grayscale,
3 for RGB, or 4 for CMYK).

Note:
    The 'sc' operator only affects the stroke color and does not impact fill operations.
    The color set by this operator is stored in the graphics state and remains in effect
    until it is changed by another color operator (e.g., 'scn' for stroke color with a specified
    color space, 'rg' for fill color, etc.). For more information on the graphics state and color
    management in PDF, refer to section 4.5 of the PDF specification.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorsc(Operator):
    """
    The 'sc' operator: Set the stroke color using the current color space.

    The 'sc' operator is used in a PDF content stream to set the stroke color for subsequent
    path operations. The color is specified using the current color space, which could be
    either a device-dependent color space (e.g., RGB or CMYK) or a device-independent color
    space (e.g., CIE-based color spaces). The 'sc' operator applies to the stroke color,
    which is used when paths are stroked with the 'S' operator or similar.

    The color values provided are based on the current color space in effect, and the operator
    expects the correct number of parameters based on the type of color space (e.g., 1 for grayscale,
    3 for RGB, or 4 for CMYK).

    Note:
        The 'sc' operator only affects the stroke color and does not impact fill operations.
        The color set by this operator is stored in the graphics state and remains in effect
        until it is changed by another color operator (e.g., 'scn' for stroke color with a specified
        color space, 'rg' for fill color, etc.). For more information on the graphics state and color
        management in PDF, refer to section 4.5 of the PDF specification.
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
        # TODO
        if source.stroke_color_space in [
            "DeviceGray",
            "CalRGB",
            "Indexed",
        ]:
            pass
        if source.stroke_color_space in [
            "DeviceRGB",
            "CalRGB",
            "Lab",
        ]:
            pass
        if source.stroke_color_space in ["DeviceCMYK"]:
            pass
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "sc"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        # TODO
        return 0
