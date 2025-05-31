#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'MP' operator: Designate a marked-content point with an associated tag.

This operator is used to designate a marked-content point in a PDF content stream. The 'tag' parameter
specifies the role or significance of the marked-content point and is represented as a name object.

Marked-content sequences are used to organize and tag content for purposes such as extracting,
filtering, or manipulating specific portions of the document. The 'MP' operator is typically used
in conjunction with other marked-content operators like 'BMC' (Begin Marked-Content) and 'EMC' (End Marked-Content)
to delineate content within the document.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorMP(Operator):
    """
    The 'MP' operator: Designate a marked-content point with an associated tag.

    This operator is used to designate a marked-content point in a PDF content stream. The 'tag' parameter
    specifies the role or significance of the marked-content point and is represented as a name object.

    Marked-content sequences are used to organize and tag content for purposes such as extracting,
    filtering, or manipulating specific portions of the document. The 'MP' operator is typically used
    in conjunction with other marked-content operators like 'BMC' (Begin Marked-Content) and 'EMC' (End Marked-Content)
    to delineate content within the document.
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
        assert isinstance(operands[0], name)
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "MP"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
