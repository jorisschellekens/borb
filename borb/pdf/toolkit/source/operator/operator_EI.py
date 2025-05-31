#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'EI' operator: End an inline image object.

The 'EI' operator is used in a PDF content stream to mark the end of an inline image object.
It signifies that the inline image object has been fully defined and is now complete.

This operator follows the 'BI' (Begin Inline Image) operator, which starts an inline image object.
After the 'EI' operator, no more content for the inline image should be processed.
This operator is critical for ensuring the proper structure and integrity of inline images in a PDF document.

Inline image objects are used to embed image data directly into the content stream,
and the 'EI' operator indicates the completion of the image's content definition.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorEI(Operator):
    """
    The 'EI' operator: End an inline image object.

    The 'EI' operator is used in a PDF content stream to mark the end of an inline image object.
    It signifies that the inline image object has been fully defined and is now complete.

    This operator follows the 'BI' (Begin Inline Image) operator, which starts an inline image object.
    After the 'EI' operator, no more content for the inline image should be processed.
    This operator is critical for ensuring the proper structure and integrity of inline images in a PDF document.

    Inline image objects are used to embed image data directly into the content stream,
    and the 'EI' operator indicates the completion of the image's content definition.
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
        return "EI"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
