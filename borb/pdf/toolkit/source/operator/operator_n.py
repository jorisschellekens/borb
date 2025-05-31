#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'n' operator: End the path without filling or stroking.

This operator is used to end a path object without performing any fill or stroke operations.
It is primarily used for the side effect of changing the current clipping path.

When this operator is used, the current path is closed without any modification to the
path's appearance. However, it can affect the current clipping path, which is used to
determine the visible area when rendering subsequent content.

The 'n' operator is typically used in conjunction with other path construction operators
to define complex clipping regions, and its primary role is in the context of clipping
path operations.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorn(Operator):
    """
    The 'n' operator: End the path without filling or stroking.

    This operator is used to end a path object without performing any fill or stroke operations.
    It is primarily used for the side effect of changing the current clipping path.

    When this operator is used, the current path is closed without any modification to the
    path's appearance. However, it can affect the current clipping path, which is used to
    determine the visible area when rendering subsequent content.

    The 'n' operator is typically used in conjunction with other path construction operators
    to define complex clipping regions, and its primary role is in the context of clipping
    path operations.
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
        source.path = []
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "n"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
