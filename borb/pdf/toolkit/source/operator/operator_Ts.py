#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Ts' operator: Set text rise.

This operator sets the text rise in the current text state, which is the amount
by which the text is displaced vertically from its baseline. The text rise is typically
used to adjust the vertical position of the text, allowing for raised or lowered text
relative to its normal position.

The operand for this operator is a numeric value that specifies the vertical offset
(rise) in user space. A positive value moves the text upward, while a negative value
moves the text downward.

Note:
    - The text rise value affects all subsequent text show operations until it is changed
      by another 'Ts' operator.
    - This operator does not affect the position of other graphic objects or the text baseline.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTs(Operator):
    """
    The 'Ts' operator: Set text rise.

    This operator sets the text rise in the current text state, which is the amount
    by which the text is displaced vertically from its baseline. The text rise is typically
    used to adjust the vertical position of the text, allowing for raised or lowered text
    relative to its normal position.

    The operand for this operator is a numeric value that specifies the vertical offset
    (rise) in user space. A positive value moves the text upward, while a negative value
    moves the text downward.

    Note:
        - The text rise value affects all subsequent text show operations until it is changed
          by another 'Ts' operator.
        - This operator does not affect the position of other graphic objects or the text baseline.
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
        # Set text rise
        assert isinstance(operands[0], float) or isinstance(operands[0], int)
        source.text_rise = operands[0]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Ts"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
