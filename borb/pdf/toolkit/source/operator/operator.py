#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a generic superclass for PDF operators.

Operators in a PDF content stream define specific actions or transformations
that modify the appearance or content of a PDF page. Examples include setting
text properties, drawing graphics, or manipulating the graphics state.

The `Operator` class provides a base structure for implementing various PDF operators,
including methods for retrieving the operator's name, determining the number of
expected operands, and applying the operator's logic.

Subclasses should override the `apply` method to implement the specific behavior of
each operator.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.source import Source


class Operator:
    """
    Represents a generic superclass for PDF operators.

    Operators in a PDF content stream define specific actions or transformations
    that modify the appearance or content of a PDF page. Examples include setting
    text properties, drawing graphics, or manipulating the graphics state.

    The `Operator` class provides a base structure for implementing various PDF operators,
    including methods for retrieving the operator's name, determining the number of
    expected operands, and applying the operator's logic.

    Subclasses should override the `apply` method to implement the specific behavior of
    each operator.
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
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return ""

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
