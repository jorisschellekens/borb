#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'EMC' operator: End a marked-content sequence.

The 'EMC' operator is used in a PDF content stream to mark the end of a marked-content sequence that was initiated
by either the 'BMC' (Begin Marked-Content) or 'BDC' (Begin Marked-Content with Property List) operator.

This operator signals the closure of the marked-content sequence,
and it ensures that the content between the 'BMC'/'BDC' and 'EMC' operators is properly associated with the specified tag
and properties (if any). The 'EMC' operator is typically used to delineate sections of content that can be treated as a unit for processing,
such as a group of related graphical elements or annotations.

It is important to note that 'EMC' does not affect the graphics state or the flow of content in the document;
it simply marks the end of the tagged content sequence.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorEMC(Operator):
    """
    The 'EMC' operator: End a marked-content sequence.

    The 'EMC' operator is used in a PDF content stream to mark the end of a marked-content sequence that was initiated
    by either the 'BMC' (Begin Marked-Content) or 'BDC' (Begin Marked-Content with Property List) operator.

    This operator signals the closure of the marked-content sequence,
    and it ensures that the content between the 'BMC'/'BDC' and 'EMC' operators is properly associated with the specified tag
    and properties (if any). The 'EMC' operator is typically used to delineate sections of content that can be treated as a unit for processing,
    such as a group of related graphical elements or annotations.

    It is important to note that 'EMC' does not affect the graphics state or the flow of content in the document;
    it simply marks the end of the tagged content sequence.
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
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "EMC"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
