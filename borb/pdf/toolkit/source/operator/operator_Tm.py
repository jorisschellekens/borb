#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Tm' operator: Set the text matrix and text line matrix.

This operator sets the text matrix (Tm) and the text line matrix (Tlm) to the specified
values. These matrices control the positioning and orientation of text. The operands
represent a matrix in the form:
    [ a b 0 ]
    [ c d 0 ]
    [ e f 1 ]
The operands are passed as six separate numbers (a, b, c, d, e, f), and the matrix
specified replaces the current text matrix and text line matrix rather than being
concatenated.

Note:
    - The initial value for Tm and Tlm is the identity matrix: [ 1 0 0 1 0 0 ].
    - This operator directly defines the transformation applied to text, influencing
      both position and scale.
"""

import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTm(Operator):
    """
    The 'Tm' operator: Set the text matrix and text line matrix.

    This operator sets the text matrix (Tm) and the text line matrix (Tlm) to the specified
    values. These matrices control the positioning and orientation of text. The operands
    represent a matrix in the form:
        [ a b 0 ]
        [ c d 0 ]
        [ e f 1 ]
    The operands are passed as six separate numbers (a, b, c, d, e, f), and the matrix
    specified replaces the current text matrix and text line matrix rather than being
    concatenated.

    Note:
        - The initial value for Tm and Tlm is the identity matrix: [ 1 0 0 1 0 0 ].
        - This operator directly defines the transformation applied to text, influencing
          both position and scale.
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
        assert isinstance(operands[2], float) or isinstance(operands[2], int)
        assert isinstance(operands[3], float) or isinstance(operands[3], int)
        assert isinstance(operands[4], float) or isinstance(operands[4], int)
        assert isinstance(operands[5], float) or isinstance(operands[5], int)
        a: typing.Union[float, int] = operands[0]
        b: typing.Union[float, int] = operands[1]
        c: typing.Union[float, int] = operands[2]
        d: typing.Union[float, int] = operands[3]
        e: typing.Union[float, int] = operands[4]
        f: typing.Union[float, int] = operands[5]
        source.text_matrix = [
            [a, b, 0.0],
            [c, d, 0.0],
            [e, f, 1.0],
        ]
        source.text_line_matrix = [
            [a, b, 0.0],
            [c, d, 0.0],
            [e, f, 1.0],
        ]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Tm"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 6
