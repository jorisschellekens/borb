#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Td' operator: Move to the start of the next line, offset by (tx, ty).

This operator moves the current text position by the specified horizontal (tx)
and vertical (ty) distances in unscaled text space units. The operands tx and ty
are values in the current text space, and they represent the offset from the
current text position to the next starting point of the text.

The effect of this operator is to displace the text position horizontally by tx
and vertically by ty. It does not modify the text leading (vertical spacing between
lines of text), unlike the 'TD' operator, which sets the leading as well.

Note:
    Both tx and ty are measured in unscaled text space units, meaning they are
    subject to the current text scaling factors in effect. The text position is
    then updated accordingly.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTd(Operator):
    """
    The 'Td' operator: Move to the start of the next line, offset by (tx, ty).

    This operator moves the current text position by the specified horizontal (tx)
    and vertical (ty) distances in unscaled text space units. The operands tx and ty
    are values in the current text space, and they represent the offset from the
    current text position to the next starting point of the text.

    The effect of this operator is to displace the text position horizontally by tx
    and vertically by ty. It does not modify the text leading (vertical spacing between
    lines of text), unlike the 'TD' operator, which sets the leading as well.

    Note:
        Both tx and ty are measured in unscaled text space units, meaning they are
        subject to the current text scaling factors in effect. The text position is
        then updated accordingly.
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
        tx: typing.Union[float, int] = operands[0]
        ty: typing.Union[float, int] = operands[1]
        source.text_line_matrix = self.__mul(
            m0=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [tx, ty, 1.0]],
            m1=source.text_line_matrix,
        )
        import copy

        source.text_matrix = copy.deepcopy(source.text_line_matrix)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Td"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
