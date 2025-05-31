#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'TD' operator: Move to the start of the next line, offset by (tx, ty).

This operator moves the current text position to a new location, offset from the
current position by the specified horizontal (tx) and vertical (ty) distances.
Additionally, it sets the leading (vertical spacing between lines of text) to the
value of ty.

This operator is equivalent to executing the following two operators in sequence:
    - -ty TL  (sets the leading to -ty)
    - tx ty Td (moves the text position by tx, ty)

Note:
    The horizontal movement (tx) and vertical movement (ty) specify the displacement
    from the current text position, allowing for precise control over text placement.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTD(Operator):
    """
    The 'TD' operator: Move to the start of the next line, offset by (tx, ty).

    This operator moves the current text position to a new location, offset from the
    current position by the specified horizontal (tx) and vertical (ty) distances.
    Additionally, it sets the leading (vertical spacing between lines of text) to the
    value of ty.

    This operator is equivalent to executing the following two operators in sequence:
        - -ty TL  (sets the leading to -ty)
        - tx ty Td (moves the text position by tx, ty)

    Note:
        The horizontal movement (tx) and vertical movement (ty) specify the displacement
        from the current text position, allowing for precise control over text placement.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_TL(leading: typing.Union[float, int], page: Page, source: Source):
        TL_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "TL"]),
            None,
        )
        assert TL_operator is not None
        TL_operator.apply(
            page=page,
            source=source,
            operands=[leading],
        )
        pass

    @staticmethod
    def __apply_Td(
        page: Page,
        source: Source,
        tx: typing.Union[float, int],
        ty: typing.Union[float, int],
    ):
        Td_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "Td"]),
            None,
        )
        assert Td_operator is not None
        Td_operator.apply(
            page=page,
            source=source,
            operands=[tx, ty],
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
        tx: typing.Union[float, int] = operands[0]
        ty: typing.Union[float, int] = operands[1]
        self.__apply_TL(
            leading=-ty,
            page=page,
            source=source,
        )
        self.__apply_Td(page=page, source=source, tx=tx, ty=ty)
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "TD"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
