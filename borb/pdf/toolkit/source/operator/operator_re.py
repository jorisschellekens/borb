#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 're' operator: Append a rectangle to the current path.

This operator appends a rectangle to the current path as a complete subpath.
The rectangle is defined by its lower-left corner at coordinates (x, y),
with the specified width and height, all in user space coordinates.

The operation `x y width height re` is equivalent to the following sequence:
    - Move to (x, y) with the 'm' operator.
    - Draw a line to (x + width, y) with the 'l' operator.
    - Draw a line to (x + width, y + height) with the 'l' operator.
    - Draw a line to (x, y + height) with the 'l' operator.
    - Close the subpath with the 'h' operator.

This operator is commonly used to create rectangular shapes within a path for
subsequent filling, stroking, or clipping operations.

Note:
    This operator creates a closed subpath representing a rectangle. If the rectangle
    needs to be filled, stroked, or clipped, additional operators such as 'f', 'S', or 'n'
    should follow.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorre(Operator):
    """
    The 're' operator: Append a rectangle to the current path.

    This operator appends a rectangle to the current path as a complete subpath.
    The rectangle is defined by its lower-left corner at coordinates (x, y),
    with the specified width and height, all in user space coordinates.

    The operation `x y width height re` is equivalent to the following sequence:
        - Move to (x, y) with the 'm' operator.
        - Draw a line to (x + width, y) with the 'l' operator.
        - Draw a line to (x + width, y + height) with the 'l' operator.
        - Draw a line to (x, y + height) with the 'l' operator.
        - Close the subpath with the 'h' operator.

    This operator is commonly used to create rectangular shapes within a path for
    subsequent filling, stroking, or clipping operations.

    Note:
        This operator creates a closed subpath representing a rectangle. If the rectangle
        needs to be filled, stroked, or clipped, additional operators such as 'f', 'S', or 'n'
        should follow.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_h(page: Page, source: Source):
        h_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "h"]),
            None,
        )
        assert h_operator is not None
        h_operator.apply(
            operands=[],
            page=page,
            source=source,
        )
        pass

    @staticmethod
    def __apply_l(
        page: Page,
        source: Source,
        x: float,
        y: float,
    ):
        l_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "l"]),
            None,
        )
        assert l_operator is not None
        l_operator.apply(
            operands=[x, y],
            page=page,
            source=source,
        )
        pass

    @staticmethod
    def __apply_m(
        page: Page,
        source: Source,
        x: float,
        y: float,
    ):
        m_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "m"]),
            None,
        )
        assert m_operator is not None
        m_operator.apply(
            operands=[x, y],
            page=page,
            source=source,
        )
        pass

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
        assert isinstance(operands[2], float) or isinstance(operands[2], int)
        assert isinstance(operands[3], float) or isinstance(operands[3], int)
        x: typing.Union[float, int] = operands[0]
        y: typing.Union[float, int] = operands[1]
        width: typing.Union[float, int] = operands[2]
        height: typing.Union[float, int] = operands[3]
        Operatorre.__apply_m(
            page=page,
            source=source,
            x=x,
            y=y,
        )
        Operatorre.__apply_l(
            page=page,
            source=source,
            x=x + width,
            y=y,
        )
        Operatorre.__apply_m(
            page=page,
            source=source,
            x=x + width,
            y=y + height,
        )
        Operatorre.__apply_m(
            page=page,
            source=source,
            x=x,
            y=y + height,
        )
        Operatorre.__apply_h(page=page, source=source)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "re"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 4
