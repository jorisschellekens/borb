#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `OperatorSingleQuote` class: Implements the `'` operator for text positioning and display.

The `'` operator in a PDF content stream moves to the next line and displays a text string.
This operator is shorthand for the sequence:

    T*
    string Tj

Where:
- `T*` moves to the start of the next line (based on the current leading).
- `Tj` displays the given text string.

This operator is typically used in text streams to simplify commands that involve moving to a new line
and displaying text in a single step.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, hexstr
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import Source


class OperatorSingleQuote(Operator):
    """
    The `OperatorSingleQuote` class: Implements the `'` operator for text positioning and display.

    The `'` operator in a PDF content stream moves to the next line and displays a text string.
    This operator is shorthand for the sequence:

        T*
        string Tj

    Where:
    - `T*` moves to the start of the next line (based on the current leading).
    - `Tj` displays the given text string.

    This operator is typically used in text streams to simplify commands that involve moving to a new line
    and displaying text in a single step.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_T_star(
        page: Page,
        source: Source,
    ):
        T_star_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "T*"]),
            None,
        )
        assert T_star_operator is not None
        T_star_operator.apply(
            operands=[],
            page=page,
            source=source,
        )

    @staticmethod
    def __apply_Tj(
        page: Page,
        source: Source,
        text_to_render: str,
    ):
        Tj_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "Tj"]),
            None,
        )
        assert Tj_operator is not None
        Tj_operator.apply(
            operands=[text_to_render],
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
        assert isinstance(operands[0], str) or isinstance(operands[0], hexstr)
        OperatorSingleQuote.__apply_T_star(page=page, source=source)
        OperatorSingleQuote.__apply_Tj(
            page=page, source=source, text_to_render=operands[0]
        )

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "'"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
