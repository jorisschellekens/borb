#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'j' operator: Set the line join style in the graphics state.

This operator sets the line join style for stroking operations in a PDF content stream.
The line join style determines how the junctions between two connected path segments
are rendered. The value of the operand specifies the join style, which can be one of the following:

- 0: Miter join (sharp corner at the junction)
- 1: Round join (a circular arc is drawn at the junction)
- 2: Bevel join (the junction is flattened at the corner)

The line join style impacts how the appearance of corners or angles between path segments is rendered.

See PDF specification section 8.4.3.4, "Line Join Style" for more details.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorj(Operator):
    """
    The 'j' operator: Set the line join style in the graphics state.

    This operator sets the line join style for stroking operations in a PDF content stream.
    The line join style determines how the junctions between two connected path segments
    are rendered. The value of the operand specifies the join style, which can be one of the following:

    - 0: Miter join (sharp corner at the junction)
    - 1: Round join (a circular arc is drawn at the junction)
    - 2: Bevel join (the junction is flattened at the corner)

    The line join style impacts how the appearance of corners or angles between path segments is rendered.

    See PDF specification section 8.4.3.4, "Line Join Style" for more details.
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
        source.line_join_style = operands[0]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "j"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
