#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'J' operator: Set the line cap style in the graphics state.

This operator sets the line cap style for stroking operations in a PDF content stream.
The line cap style determines how the ends of a stroked path are rendered.
The value of the operand specifies the cap style, which can be one of the following:

- 0: Butt cap (the stroke ends at the path's endpoint)
- 1: Round cap (a semicircular cap extends beyond the endpoint)
- 2: Square cap (a square cap extends beyond the endpoint)

The line cap style influences how paths are drawn and can impact the appearance of
closed shapes or paths with sharp corners.

See PDF specification section 8.4.3.3, "Line Cap Style" for more details.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorJ(Operator):
    """
    The 'J' operator: Set the line cap style in the graphics state.

    This operator sets the line cap style for stroking operations in a PDF content stream.
    The line cap style determines how the ends of a stroked path are rendered.
    The value of the operand specifies the cap style, which can be one of the following:

    - 0: Butt cap (the stroke ends at the path's endpoint)
    - 1: Round cap (a semicircular cap extends beyond the endpoint)
    - 2: Square cap (a square cap extends beyond the endpoint)

    The line cap style influences how paths are drawn and can impact the appearance of
    closed shapes or paths with sharp corners.

    See PDF specification section 8.4.3.3, "Line Cap Style" for more details.
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
        assert isinstance(operands[0], int)
        source.line_cap_style = operands[0]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "J"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
