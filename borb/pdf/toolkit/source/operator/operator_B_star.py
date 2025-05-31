#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'B*' operator: Fill and then stroke the path using the even-odd rule.

The 'B*' operator is used in a PDF content stream to fill and then stroke a path.
Unlike the 'B' operator, it uses the even-odd rule to determine the region to fill.
This rule considers a point inside a path if it is crossed by an odd number of path
segments, ensuring that specific overlapping regions are filled as intended.

The 'B*' operator produces the same result as the 'B' operator, except that the
path is filled as if with the 'f*' operator (even-odd fill) instead of 'f' (nonzero
winding number fill).

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


class OperatorBStar(Operator):
    """
    The 'B*' operator: Fill and then stroke the path using the even-odd rule.

    The 'B*' operator is used in a PDF content stream to fill and then stroke a path.
    Unlike the 'B' operator, it uses the even-odd rule to determine the region to fill.
    This rule considers a point inside a path if it is crossed by an odd number of path
    segments, ensuring that specific overlapping regions are filled as intended.

    The 'B*' operator produces the same result as the 'B' operator, except that the
    path is filled as if with the 'f*' operator (even-odd fill) instead of 'f' (nonzero
    winding number fill).

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
    def __apply_S(page: Page, source: Source):
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
        pass

    @staticmethod
    def __apply_f_star(page: Page, source: Source):
        f_star_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "f*"]),
            None,
        )
        assert f_star_operator is not None
        f_star_operator.apply(
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
        import copy

        path_duplicate = copy.deepcopy(source.path)
        OperatorBStar.__apply_f_star(page=page, source=source)
        source.path = path_duplicate
        OperatorBStar.__apply_S(page=page, source=source)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "B*"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
