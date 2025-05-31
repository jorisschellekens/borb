#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'T*' operator: Move to the start of the next line.

This operator moves the current point to the start of the next line by using the
current leading parameter in the text state. It has the same effect as the following
sequence:
    0 -Tl Td
where 'Tl' denotes the current leading parameter in the text state. The negative of 'Tl'
is used here because 'Tl' is the text leading expressed as a positive number. Moving to
the next line entails decreasing the y coordinate.

Note:
    The operator adjusts the position by the leading, effectively starting the next line
    of text relative to the current line's end point.
"""

import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTStar(Operator):
    """
    The 'T*' operator: Move to the start of the next line.

    This operator moves the current point to the start of the next line by using the
    current leading parameter in the text state. It has the same effect as the following
    sequence:
        0 -Tl Td
    where 'Tl' denotes the current leading parameter in the text state. The negative of 'Tl'
    is used here because 'Tl' is the text leading expressed as a positive number. Moving to
    the next line entails decreasing the y coordinate.

    Note:
        The operator adjusts the position by the leading, effectively starting the next line
        of text relative to the current line's end point.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_Td(
        page: Page,
        source: Source,
        tx: float,
        ty: float,
    ):
        Td_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "Td"]),
            None,
        )
        assert Td_operator is not None
        Td_operator.apply(
            operands=[tx, ty],
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
        OperatorTStar.__apply_Td(
            page=page,
            source=source,
            tx=0,
            ty=-source.leading,
        )
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "T*"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
