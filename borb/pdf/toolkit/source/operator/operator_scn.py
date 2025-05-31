#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'scn' operator: Set the color for nonstroking operations in special color spaces (ICCBased, Separation, DeviceN, and Pattern).

This operator sets the current color for nonstroking operations in advanced color spaces, including ICCBased,
Separation, DeviceN, and Pattern. The number and interpretation of the operands depend on the current nonstroking
color space:

- For Separation, DeviceN, or ICCBased color spaces, the operands (c1...cn) are numbers that specify the
  color components.
- For Pattern color spaces, the first operand is a name (representing an entry in the Pattern subdictionary of the
  current resource dictionary). If the pattern is uncolored (PatternType = 1 and PaintType = 2), additional operands
  specify the color in the pattern’s underlying color space.

The 'scn' operator updates the nonstroking color in the current graphics state and is used for filling paths,
shapes, or any other graphical elements that require special color handling.

Note:
    - The 'scn' operator is versatile and supports color spaces beyond the standard Device color spaces (RGB, CMYK, and Gray).
    - For stroking operations in these advanced color spaces, use the 'SCN' operator.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorscn(Operator):
    """
    The 'scn' operator: Set the color for nonstroking operations in special color spaces (ICCBased, Separation, DeviceN, and Pattern).

    This operator sets the current color for nonstroking operations in advanced color spaces, including ICCBased,
    Separation, DeviceN, and Pattern. The number and interpretation of the operands depend on the current nonstroking
    color space:

    - For Separation, DeviceN, or ICCBased color spaces, the operands (c1...cn) are numbers that specify the
      color components.
    - For Pattern color spaces, the first operand is a name (representing an entry in the Pattern subdictionary of the
      current resource dictionary). If the pattern is uncolored (PatternType = 1 and PaintType = 2), additional operands
      specify the color in the pattern’s underlying color space.

    The 'scn' operator updates the nonstroking color in the current graphics state and is used for filling paths,
    shapes, or any other graphical elements that require special color handling.

    Note:
        - The 'scn' operator is versatile and supports color spaces beyond the standard Device color spaces (RGB, CMYK, and Gray).
        - For stroking operations in these advanced color spaces, use the 'SCN' operator.
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
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "scn"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        # TODO
        return 0
