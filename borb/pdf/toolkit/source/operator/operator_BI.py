#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'BI' operator: Begin an inline image object.

The 'BI' operator is used to start an inline image object in a PDF content stream.
It marks the beginning of the data for an inline image that will be embedded directly
in the content stream. The inline image data is typically followed by an associated
dictionary describing the image's properties, such as width, height, color space, etc.

The inline image data is terminated by the 'EI' operator, which marks the end of the inline image.

Note:
    This operator is used in cases where the image data is included directly within
    the content stream, as opposed to being referenced externally.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorBI(Operator):
    """
    The 'BI' operator: Begin an inline image object.

    The 'BI' operator is used to start an inline image object in a PDF content stream.
    It marks the beginning of the data for an inline image that will be embedded directly
    in the content stream. The inline image data is typically followed by an associated
    dictionary describing the image's properties, such as width, height, color space, etc.

    The inline image data is terminated by the 'EI' operator, which marks the end of the inline image.

    Note:
        This operator is used in cases where the image data is included directly within
        the content stream, as opposed to being referenced externally.
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
        return "BI"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
