#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 's' operator: Close and stroke the path.

This operator is used to close the current subpath by appending a straight line
segment from the current point to the starting point of the subpath and then
strokes the resulting path. If the current subpath is already closed, the operator
simply strokes the path.

This operator has the same effect as executing the sequence 'h S', where 'h' closes
the current subpath, and 'S' strokes the path.

Note:
    The behavior of this operator depends on the current graphics state parameters,
    such as the current line width, color, and dash pattern.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operators(Operator):
    """
    The 's' operator: Close and stroke the path.

    This operator is used to close the current subpath by appending a straight line
    segment from the current point to the starting point of the subpath and then
    strokes the resulting path. If the current subpath is already closed, the operator
    simply strokes the path.

    This operator has the same effect as executing the sequence 'h S', where 'h' closes
    the current subpath, and 'S' strokes the path.

    Note:
        The behavior of this operator depends on the current graphics state parameters,
        such as the current line width, color, and dash pattern.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_S(
        page: Page,
        source: Source,
    ):
        S_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "S"]),
            None,
        )
        assert S_operator is not None
        S_operator.apply(
            operands=[],
            page=page,
            source=source,
        )

    @staticmethod
    def __apply_h(
        page: Page,
        source: Source,
    ):
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
        Operators.__apply_h(page=page, source=source)
        Operators.__apply_S(page=page, source=source)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "s"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
