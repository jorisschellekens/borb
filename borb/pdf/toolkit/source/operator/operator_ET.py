#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'ET' operator: End a text object.

The 'ET' operator is used in a PDF content stream to signify the end of a text object.
It terminates the current text object and discards the associated text matrix (Tm) and
text line matrix (Tlm), resetting the text state.

Text objects are initialized with the 'BT' (Begin Text) operator and represent sequences
of text-related operations. Once 'ET' is called, the text-specific state is cleared, and
the content stream continues with other graphics or text operations.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorET(Operator):
    """
    The 'ET' operator: End a text object.

    The 'ET' operator is used in a PDF content stream to signify the end of a text object.
    It terminates the current text object and discards the associated text matrix (Tm) and
    text line matrix (Tlm), resetting the text state.

    Text objects are initialized with the 'BT' (Begin Text) operator and represent sequences
    of text-related operations. Once 'ET' is called, the text-specific state is cleared, and
    the content stream continues with other graphics or text operations.
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
        source.text_matrix = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        source.text_line_matrix = [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "ET"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
