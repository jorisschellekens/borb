#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'S' operator: Stroke the path.

This operator is used in a PDF content stream to stroke the current path. The path
is outlined using the current graphics state parameters, such as the current line width,
line color, and dash pattern, and the path is drawn along the defined path coordinates.

The operator does not fill the path; it only paints the path outline.

Note:
    The behavior of this operator depends on several graphics state parameters,
    including the current color, line width, line join, and dash pattern.
    See the section on "Path-Painting Operators" for more details on how the path
    is stroked.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorS(Operator):
    """
    The 'S' operator: Stroke the path.

    This operator is used in a PDF content stream to stroke the current path. The path
    is outlined using the current graphics state parameters, such as the current line width,
    line color, and dash pattern, and the path is drawn along the defined path coordinates.

    The operator does not fill the path; it only paints the path outline.

    Note:
        The behavior of this operator depends on several graphics state parameters,
        including the current color, line width, line join, and dash pattern.
        See the section on "Path-Painting Operators" for more details on how the path
        is stroked.
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
        while len(source.path) > 0:
            source.stroke(
                line_width=source.line_width,
                shape=source.path[0],
                stroke_color=source.stroke_color,
            )
            source.path.pop(0)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "S"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
