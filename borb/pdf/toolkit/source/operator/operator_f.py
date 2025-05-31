#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'f' operator: Fill the current path.

This operator fills the current path using the nonzero winding number rule,
determining the regions to be painted. Before filling, any open subpaths in
the path are implicitly closed.

The nonzero winding number rule considers the direction in which the path
is drawn to determine the regions to fill. See section 8.5.3.3.2, "Nonzero Winding
Number Rule," in the PDF specification for further details.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
    PointType,
)


class Operatorf(Operator):
    """
    The 'f' operator: Fill the current path.

    This operator fills the current path using the nonzero winding number rule,
    determining the regions to be painted. Before filling, any open subpaths in
    the path are implicitly closed.

    The nonzero winding number rule considers the direction in which the path
    is drawn to determine the regions to fill. See section 8.5.3.3.2, "Nonzero Winding
    Number Rule," in the PDF specification for further details.
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
        for i in range(0, len(source.path)):
            p0: PointType = source.path[i][0][0]
            pn: PointType = source.path[i][-1][-1]
            d: float = (p0[0] - pn[0]) ** 2 + (p0[1] - pn[1]) ** 2
            if d < 1 * 10**-5:
                continue
            source.path[i] += [(pn, p0)]
        while len(source.path) > 0:
            source.fill(
                fill_color=source.non_stroke_color,
                shape=source.path[0],
                use_even_odd_rule=False,
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
        return "f"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
