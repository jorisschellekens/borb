#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'F' operator: Equivalent to 'f' (fill the path).

The 'F' operator is functionally identical to the 'f' operator, which fills the current path
using the nonzero winding number rule. This operator is included solely for compatibility
with older implementations.

Note:
    While PDF reader applications must support this operator, PDF writer applications
    are encouraged to use 'f' instead.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorF(Operator):
    """
    The 'F' operator: Equivalent to 'f' (fill the path).

    The 'F' operator is functionally identical to the 'f' operator, which fills the current path
    using the nonzero winding number rule. This operator is included solely for compatibility
    with older implementations.

    Note:
        While PDF reader applications must support this operator, PDF writer applications
        are encouraged to use 'f' instead.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_f(page: Page, source: Source):
        f_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "f"]),
            None,
        )
        assert f_operator is not None
        f_operator.apply(
            page=page,
            source=source,
            operands=[],
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
        OperatorF.__apply_f(page=page, source=source)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "F"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
