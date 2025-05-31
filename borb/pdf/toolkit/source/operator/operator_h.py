#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'h' operator: Close the current subpath.

This operator closes the current subpath by appending a straight line segment from the
current point to the starting point of the subpath. If the subpath is already closed,
the operator does nothing.

Notes:
    - The 'h' operator terminates the current subpath. Any subsequent segment added
      to the path will start a new subpath, even if it begins at the endpoint reached
      by the 'h' operation.
    - This operator is useful for completing shapes without explicitly drawing the
      closing line segment.

Refer to the PDF specification for further details on path construction and the
role of subpaths.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorh(Operator):
    """
    The 'h' operator: Close the current subpath.

    This operator closes the current subpath by appending a straight line segment from the
    current point to the starting point of the subpath. If the subpath is already closed,
    the operator does nothing.

    Notes:
        - The 'h' operator terminates the current subpath. Any subsequent segment added
          to the path will start a new subpath, even if it begins at the endpoint reached
          by the 'h' operation.
        - This operator is useful for completing shapes without explicitly drawing the
          closing line segment.

    Refer to the PDF specification for further details on path construction and the
    role of subpaths.
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
        if len(source.path) == 0:
            return
        p0 = source.path[-1][0][0]
        pn = source.path[-1][-1][-1]
        d: float = (p0[0] - pn[0]) ** 2 + (p0[1] - pn[1]) ** 2
        if d < 1 * 10**-5:
            return
        source.path[-1] += [(pn, p0)]
        source.path += []
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "h"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
