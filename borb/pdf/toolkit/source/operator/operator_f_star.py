#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'f*' operator: Fill the current path using the even-odd rule.

This operator fills the current path using the even-odd rule to determine the
regions to be painted. The even-odd rule defines a region as filled if a ray
drawn from any point within the region to infinity crosses the path an odd number
of times.

See section 8.5.3.3.3, "Even-Odd Rule," in the PDF specification for more details.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorfStar(Operator):
    """
    The 'f*' operator: Fill the current path using the even-odd rule.

    This operator fills the current path using the even-odd rule to determine the
    regions to be painted. The even-odd rule defines a region as filled if a ray
    drawn from any point within the region to infinity crosses the path an odd number
    of times.

    See section 8.5.3.3.3, "Even-Odd Rule," in the PDF specification for more details.
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
        while len(source.path) > 0:
            source.fill(
                fill_color=source.non_stroke_color,
                shape=source.path[0],
                use_even_odd_rule=True,
            )
            source.path.pop(0)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "f*"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
