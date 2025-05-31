#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'BT' operator: Begin a text object and initialize the text matrix and text line matrix.

The 'BT' (Begin Text) operator is used to begin a text object in a PDF content stream.
It initializes the text matrix (Tm) and the text line matrix (Tlm) to the identity matrix,
which sets up the coordinate system for positioning and rendering text.

After the 'BT' operator, text-related operators can be used to set the font, size, color,
and other properties related to text rendering. The text object is ended with the 'ET' operator.

Note:
    Text objects cannot be nested. A second 'BT' operator cannot appear before an 'ET' operator
    has been encountered to close the first text object.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorBT(Operator):
    """
    The 'BT' operator: Begin a text object and initialize the text matrix and text line matrix.

    The 'BT' (Begin Text) operator is used to begin a text object in a PDF content stream.
    It initializes the text matrix (Tm) and the text line matrix (Tlm) to the identity matrix,
    which sets up the coordinate system for positioning and rendering text.

    After the 'BT' operator, text-related operators can be used to set the font, size, color,
    and other properties related to text rendering. The text object is ended with the 'ET' operator.

    Note:
        Text objects cannot be nested. A second 'BT' operator cannot appear before an 'ET' operator
        has been encountered to close the first text object.
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
        return "BT"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
