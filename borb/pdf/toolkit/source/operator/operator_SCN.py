#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'SCN' operator: Set the color for stroking operations, supporting additional color spaces.

This operator functions like the 'SC' operator but also supports Pattern, Separation,
DeviceN, and ICCBased color spaces. The number of operands and their interpretation
depend on the current stroking color space.

If the current stroking color space is:

- **Separation**, **DeviceN**, or **ICCBased**: The operands (c1…cn) are numbers, and
  the number of operands varies depending on the color space.
- **Pattern color space**: The operand is the name of an entry in the Pattern subdictionary
  of the current resource dictionary. For an uncolored tiling pattern (PatternType = 1,
  PaintType = 2), the operands (c1…cn) specify a color in the pattern’s underlying color space.
  For other types of patterns, no operands are specified.

The operator sets the color for stroking operations, affecting the current graphics state.

Note:
    The behavior of this operator is influenced by the specifics of the stroking
    color space, which can vary significantly in terms of operands and their meanings.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorSCN(Operator):
    """
    The 'SCN' operator: Set the color for stroking operations, supporting additional color spaces.

    This operator functions like the 'SC' operator but also supports Pattern, Separation,
    DeviceN, and ICCBased color spaces. The number of operands and their interpretation
    depend on the current stroking color space.

    If the current stroking color space is:

    - **Separation**, **DeviceN**, or **ICCBased**: The operands (c1…cn) are numbers, and
      the number of operands varies depending on the color space.
    - **Pattern color space**: The operand is the name of an entry in the Pattern subdictionary
      of the current resource dictionary. For an uncolored tiling pattern (PatternType = 1,
      PaintType = 2), the operands (c1…cn) specify a color in the pattern’s underlying color space.
      For other types of patterns, no operands are specified.

    The operator sets the color for stroking operations, affecting the current graphics state.

    Note:
        The behavior of this operator is influenced by the specifics of the stroking
        color space, which can vary significantly in terms of operands and their meanings.
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
        return "SCN"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        # TODO
        return 0
