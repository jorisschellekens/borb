#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'g' operator: Set the nonstroking gray level.

This operator sets the current nonstroking color space to DeviceGray (or the DefaultGray
color space, as specified in section 8.6.5.6, "Default Colour Spaces") and assigns
a gray level for nonstroking operations. The `gray` operand must be a number between
0.0 (black) and 1.0 (white).

This operator is commonly used for setting fill colors in grayscale.
"""
import typing

from borb.pdf.color.grayscale_color import GrayscaleColor
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorg(Operator):
    """
    The 'g' operator: Set the nonstroking gray level.

    This operator sets the current nonstroking color space to DeviceGray (or the DefaultGray
    color space, as specified in section 8.6.5.6, "Default Colour Spaces") and assigns
    a gray level for nonstroking operations. The `gray` operand must be a number between
    0.0 (black) and 1.0 (white).

    This operator is commonly used for setting fill colors in grayscale.
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
        level: float = operands[0]
        source.non_stroke_color_space = name("DeviceGray")
        source.non_stroke_color = GrayscaleColor(level)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "g"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
