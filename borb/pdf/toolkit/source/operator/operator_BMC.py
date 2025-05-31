#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'BMC' operator: Begin a marked-content sequence terminated by a balancing 'EMC' operator.

The 'BMC' operator is used to begin a marked-content sequence in a PDF content stream.
The sequence is terminated by the 'EMC' (End Marked Content) operator, which balances
the 'BMC' operator. The 'tag' parameter, passed as a name object, indicates the role
or significance of the marked-content sequence.

Marked-content sequences are used to associate metadata or other relevant information
with specific content in the document. This can include annotations, tags for accessibility,
or other document-specific data.

Note:
    Marked-content sequences allow for better structure and accessibility in PDF documents.
    The 'tag' is typically used to identify the nature of the content, and the sequence
    can be used to apply properties or metadata to the content within the sequence.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorBMC(Operator):
    """
    The 'BMC' operator: Begin a marked-content sequence terminated by a balancing 'EMC' operator.

    The 'BMC' operator is used to begin a marked-content sequence in a PDF content stream.
    The sequence is terminated by the 'EMC' (End Marked Content) operator, which balances
    the 'BMC' operator. The 'tag' parameter, passed as a name object, indicates the role
    or significance of the marked-content sequence.

    Marked-content sequences are used to associate metadata or other relevant information
    with specific content in the document. This can include annotations, tags for accessibility,
    or other document-specific data.

    Note:
        Marked-content sequences allow for better structure and accessibility in PDF documents.
        The 'tag' is typically used to identify the nature of the content, and the sequence
        can be used to apply properties or metadata to the content within the sequence.
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
        return "BMC"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
