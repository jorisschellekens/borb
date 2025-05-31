#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'd0' operator: Set width information for the glyph and declare that the glyph description specifies both its shape and its colour.

The 'd0' operator is used in Type 3 fonts within a PDF content stream to specify the width of a glyph and to declare
that the glyph's description defines both its shape and its colour. Specifically, this operator sets the horizontal
displacement (wx) of the glyph in the glyph coordinate system, which should match the corresponding value in the
font's Widths array. The vertical displacement (wy) is always set to 0.

This operator is typically used when the glyph description in the Type 3 font executes operators that explicitly set
the glyph's colour.

Note:
    - The 'd0' operator must only be used in a content stream found in a Type 3 font's CharProcs dictionary.
    - The operator name ends with the digit '0' to indicate this specific behavior.
    - For more details on glyph positioning and metrics, refer to PDF specification section 9.2.4, "Glyph Positioning and Metrics."
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatord0(Operator):
    """
    The 'd0' operator: Set width information for the glyph and declare that the glyph description specifies both its shape and its colour.

    The 'd0' operator is used in Type 3 fonts within a PDF content stream to specify the width of a glyph and to declare
    that the glyph's description defines both its shape and its colour. Specifically, this operator sets the horizontal
    displacement (wx) of the glyph in the glyph coordinate system, which should match the corresponding value in the
    font's Widths array. The vertical displacement (wy) is always set to 0.

    This operator is typically used when the glyph description in the Type 3 font executes operators that explicitly set
    the glyph's colour.

    Note:
        - The 'd0' operator must only be used in a content stream found in a Type 3 font's CharProcs dictionary.
        - The operator name ends with the digit '0' to indicate this specific behavior.
        - For more details on glyph positioning and metrics, refer to PDF specification section 9.2.4, "Glyph Positioning and Metrics."
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
        assert isinstance(operands[1], float) or isinstance(operands[1], int)
        wx: typing.Union[float, int] = operands[0]
        wy: typing.Union[float, int] = operands[1]
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "d0"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
