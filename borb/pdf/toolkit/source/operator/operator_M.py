#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'M' operator: Set the miter limit in the graphics state.

This operator sets the miter limit in the graphics state, which controls how the intersection of two connected
path segments is joined when the line join style is set to miter. The miter limit defines the maximum allowed
length for the miter (the sharp point at the intersection of two path segments). If the miter exceeds this limit,
the line join is automatically converted to a bevel join.

The operand specifies the miter limit value, which is a positive number.

The miter limit is used when the line join style is set to "miter" (using the `j` operator) and affects how sharp
the corners are when two lines meet at an angle.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorM(Operator):
    """
    The 'M' operator: Set the miter limit in the graphics state.

    This operator sets the miter limit in the graphics state, which controls how the intersection of two connected
    path segments is joined when the line join style is set to miter. The miter limit defines the maximum allowed
    length for the miter (the sharp point at the intersection of two path segments). If the miter exceeds this limit,
    the line join is automatically converted to a bevel join.

    The operand specifies the miter limit value, which is a positive number.

    The miter limit is used when the line join style is set to "miter" (using the `j` operator) and affects how sharp
    the corners are when two lines meet at an angle.
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
        source.miter_limit = operands[0]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "M"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
