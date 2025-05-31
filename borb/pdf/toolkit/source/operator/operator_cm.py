#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'cm' operator: Modify the current transformation matrix (CTM).

The 'cm' operator is used to modify the current transformation matrix (CTM) by concatenating
it with the specified matrix. The operands of this operator are six numbers that represent
the matrix to be concatenated with the current CTM (not an array).

This operator allows for transformations of the coordinate system, such as scaling, rotation,
and translation, as described in PDF specification section 8.3.2, "Coordinate Spaces".

The six operands are provided in the following order:
    - a, b, c, d: The elements of the 2x2 transformation matrix.
    - e, f: The translation components of the transformation.

After the operator is executed, the CTM is updated to reflect the transformation.

Note:
    Refer to PDF specification section 8.3.2, "Coordinate Spaces", for more information
    on how coordinate transformations are applied in PDF graphics.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorcm(Operator):
    """
    The 'cm' operator: Modify the current transformation matrix (CTM).

    The 'cm' operator is used to modify the current transformation matrix (CTM) by concatenating
    it with the specified matrix. The operands of this operator are six numbers that represent
    the matrix to be concatenated with the current CTM (not an array).

    This operator allows for transformations of the coordinate system, such as scaling, rotation,
    and translation, as described in PDF specification section 8.3.2, "Coordinate Spaces".

    The six operands are provided in the following order:
        - a, b, c, d: The elements of the 2x2 transformation matrix.
        - e, f: The translation components of the transformation.

    After the operator is executed, the CTM is updated to reflect the transformation.

    Note:
        Refer to PDF specification section 8.3.2, "Coordinate Spaces", for more information
        on how coordinate transformations are applied in PDF graphics.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __mul(
        m0: typing.List[typing.List[float]], m1: typing.List[typing.List[float]]
    ) -> typing.List[typing.List[float]]:
        return [
            [
                m0[0][0] * m1[0][0] + m0[0][1] * m1[1][0] + m0[0][2] * m1[2][0],
                m0[0][0] * m1[0][1] + m0[0][1] * m1[1][1] + m0[0][2] * m1[2][1],
                m0[0][0] * m1[0][2] + m0[0][1] * m1[1][2] + m0[0][2] * m1[2][2],
            ],
            [
                m0[1][0] * m1[0][0] + m0[1][1] * m1[1][0] + m0[1][2] * m1[2][0],
                m0[1][0] * m1[0][1] + m0[1][1] * m1[1][1] + m0[1][2] * m1[2][1],
                m0[1][0] * m1[0][2] + m0[1][1] * m1[1][2] + m0[1][2] * m1[2][2],
            ],
            [
                m0[2][0] * m1[0][0] + m0[2][1] * m1[1][0] + m0[2][2] * m1[2][0],
                m0[2][0] * m1[0][1] + m0[2][1] * m1[1][1] + m0[2][2] * m1[2][1],
                m0[2][0] * m1[0][2] + m0[2][1] * m1[1][2] + m0[2][2] * m1[2][2],
            ],
        ]

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
        source.transformation_matrix = Operatorcm.__mul(
            source.transformation_matrix,
            [[a, b, 0], [c, d, 0], [e, f, 1]],
        )
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "cm"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 6
