#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'BX' operator: Begin a compatibility section.

The 'BX' (Begin Compatibility) operator is used to start a compatibility section in a PDF
content stream. This section allows the inclusion of unrecognized operators and their operands,
which will be ignored without generating errors until the balancing 'EX' operator is encountered.
This feature is particularly useful for backward compatibility with older versions of PDF.

Note:
    The operators and operands in the compatibility section will not affect the rendering
    of the page or other operations until the 'EX' operator is encountered, which ends
    the compatibility section.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorBX(Operator):
    """
    The 'BX' operator: Begin a compatibility section.

    The 'BX' (Begin Compatibility) operator is used to start a compatibility section in a PDF
    content stream. This section allows the inclusion of unrecognized operators and their operands,
    which will be ignored without generating errors until the balancing 'EX' operator is encountered.
    This feature is particularly useful for backward compatibility with older versions of PDF.

    Note:
        The operators and operands in the compatibility section will not affect the rendering
        of the page or other operations until the 'EX' operator is encountered, which ends
        the compatibility section.
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
        source.is_in_compatibility_section = True
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "BX"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
