#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'd' operator: Set the line dash pattern in the graphics state.

The 'd' operator is used to define the dash pattern for lines in a PDF content stream. This operator sets the
line dash pattern in the graphics state, specifying how the strokes of paths will be drawn. The pattern is
defined by a sequence of numbers, where the even-indexed numbers represent the lengths of the dashes and
the odd-indexed numbers represent the lengths of the gaps between dashes.

This operator is typically followed by operands specifying the dash pattern and the phase value, which determines
where the pattern starts along the path.

Note:
    For more details on line dash patterns, refer to PDF specification section 8.4.3.6, "Line Dash Pattern."
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatord(Operator):
    """
    The 'd' operator: Set the line dash pattern in the graphics state.

    The 'd' operator is used to define the dash pattern for lines in a PDF content stream. This operator sets the
    line dash pattern in the graphics state, specifying how the strokes of paths will be drawn. The pattern is
    defined by a sequence of numbers, where the even-indexed numbers represent the lengths of the dashes and
    the odd-indexed numbers represent the lengths of the gaps between dashes.

    This operator is typically followed by operands specifying the dash pattern and the phase value, which determines
    where the pattern starts along the path.

    Note:
        For more details on line dash patterns, refer to PDF specification section 8.4.3.6, "Line Dash Pattern."
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
        assert isinstance(operands[0], typing.List)
        assert isinstance(operands[1], int) or isinstance(operands[1], float)
        source.dash_array = operands[0]  # type: ignore[assignment] # TODO: parametrized generics can not be used with instance and class checks
        source.dash_phase = int(operands[1])
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "d"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
