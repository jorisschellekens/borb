#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'm' operator: Begin a new subpath by moving the current point to the specified coordinates.

This operator moves the current point to the coordinates (x, y), thereby starting a new subpath.
No connecting line segment is added between the previous point and the new point.

If the previous path construction operator was also 'm', the new 'm' operation overrides the previous one,
effectively resetting the path without any continuation of the prior subpath.

This operator is used to define the starting point of a new subpath, which is an isolated sequence of path segments.
Any further path construction operators (like `l` for line) will then create the path from this new point.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorm(Operator):
    """
    The 'm' operator: Begin a new subpath by moving the current point to the specified coordinates.

    This operator moves the current point to the coordinates (x, y), thereby starting a new subpath.
    No connecting line segment is added between the previous point and the new point.

    If the previous path construction operator was also 'm', the new 'm' operation overrides the previous one,
    effectively resetting the path without any continuation of the prior subpath.

    This operator is used to define the starting point of a new subpath, which is an isolated sequence of path segments.
    Any further path construction operators (like `l` for line) will then create the path from this new point.
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
        assert isinstance(operands[0], float) or isinstance(operands[0], int)
        assert isinstance(operands[1], float) or isinstance(operands[1], int)
        x: typing.Union[float, int] = operands[0]
        y: typing.Union[float, int] = operands[1]
        source.path += [[((x, y), (x, y))]]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "m"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
