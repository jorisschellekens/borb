#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'b' operator: Close, fill, and then stroke the path using the nonzero winding number rule.

The 'b' operator is used in a PDF content stream to close the current path, fill it,
and then stroke it. The filling portion of the operation uses the nonzero winding
number rule to determine the region to fill, ensuring that the enclosed areas are properly processed.

The 'b' operator has the same effect as the sequence `h B`, where `h` closes
the path and `B` fills and strokes it.

Note:
    The filling and stroking portions of this operation consult different values of
    several graphics state parameters, such as the current color. Refer to PDF
    specification section 11.7.4.4, "Special Path-Painting Considerations," for
    additional details on these interactions.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorb(Operator):
    """
    The 'b' operator: Close, fill, and then stroke the path using the nonzero winding number rule.

    The 'b' operator is used in a PDF content stream to close the current path, fill it,
    and then stroke it. The filling portion of the operation uses the nonzero winding
    number rule to determine the region to fill, ensuring that the enclosed areas are properly processed.

    The 'b' operator has the same effect as the sequence `h B`, where `h` closes
    the path and `B` fills and strokes it.

    Note:
        The filling and stroking portions of this operation consult different values of
        several graphics state parameters, such as the current color. Refer to PDF
        specification section 11.7.4.4, "Special Path-Painting Considerations," for
        additional details on these interactions.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_B(page: Page, source: Source):
        B_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "B"]),
            None,
        )
        assert B_operator is not None
        B_operator.apply(
            operands=[],
            page=page,
            source=source,
        )

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
        Operatorb.__apply_h(
            page=page,
            source=source,
        )
        Operatorb.__apply_B(
            page=page,
            source=source,
        )
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "b"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
