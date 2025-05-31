#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'gs' operator: Set graphics state parameters.

This operator modifies the graphics state by applying parameters from a specified graphics
state dictionary. The `dictName` operand must be a name object referencing an entry in the
ExtGState subdictionary of the current resource dictionary.

Graphics state parameters can include settings such as line width, line cap style, miter
limit, transparency, and other rendering properties.

Introduced in PDF 1.2.

Refer to the PDF specification for more details on the ExtGState subdictionary and its usage.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorgs(Operator):
    """
    The 'gs' operator: Set graphics state parameters.

    This operator modifies the graphics state by applying parameters from a specified graphics
    state dictionary. The `dictName` operand must be a name object referencing an entry in the
    ExtGState subdictionary of the current resource dictionary.

    Graphics state parameters can include settings such as line width, line cap style, miter
    limit, transparency, and other rendering properties.

    Introduced in PDF 1.2.

    Refer to the PDF specification for more details on the ExtGState subdictionary and its usage.
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
        return "gs"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
