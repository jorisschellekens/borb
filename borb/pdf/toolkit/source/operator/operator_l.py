#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'l' operator: Append a straight line segment from the current point to the specified point.

This operator appends a straight line segment to the current path, extending from the current point to a new point
specified by the operands (x, y). After executing this operator, the current point is updated to the new point (x, y).

The operands (x, y) specify the coordinates of the endpoint of the line segment to be added.

This operator is commonly used to build paths incrementally by adding straight line segments, helping to create
more complex shapes when multiple line segments are connected.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
    LineType,
    ShapeType,
    PointType,
)


class Operatorl(Operator):
    """
    The 'l' operator: Append a straight line segment from the current point to the specified point.

    This operator appends a straight line segment to the current path, extending from the current point to a new point
    specified by the operands (x, y). After executing this operator, the current point is updated to the new point (x, y).

    The operands (x, y) specify the coordinates of the endpoint of the line segment to be added.

    This operator is commonly used to build paths incrementally by adding straight line segments, helping to create
    more complex shapes when multiple line segments are connected.
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
        x: float = operands[0]
        y: float = operands[1]
        last_shape: ShapeType = source.path[-1]
        last_line: LineType = last_shape[-1]
        last_point: PointType = last_line[-1]
        source.path[-1] += [(last_point, (x, y))]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "l"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
