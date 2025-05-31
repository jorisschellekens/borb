#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The `OperatorDoubleQuote` class: Implements the `"` operator for advanced text positioning and display.

The `"` operator in a PDF content stream moves to the next line, sets the word spacing (`aw`)
and character spacing (`ac`) in the text state, and then displays a text string. The parameters
`aw` (word spacing) and `ac` (character spacing) are specified in unscaled text space units.

This operator is functionally equivalent to the following sequence:

    aw Tw
    ac Tc
    string '

Where:
- `aw Tw` sets the word spacing to `aw`.
- `ac Tc` sets the character spacing to `ac`.
- `string '` moves to the next line and displays the given text string.

This operator is commonly used to adjust spacing dynamically while rendering text in a PDF content stream.
"""

import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, hexstr
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import Source


class OperatorDoubleQuote(Operator):
    """
    The `OperatorDoubleQuote` class: Implements the `"` operator for advanced text positioning and display.

    The `"` operator in a PDF content stream moves to the next line, sets the word spacing (`aw`)
    and character spacing (`ac`) in the text state, and then displays a text string. The parameters
    `aw` (word spacing) and `ac` (character spacing) are specified in unscaled text space units.

    This operator is functionally equivalent to the following sequence:

        aw Tw
        ac Tc
        string '

    Where:
    - `aw Tw` sets the word spacing to `aw`.
    - `ac Tc` sets the character spacing to `ac`.
    - `string '` moves to the next line and displays the given text string.

    This operator is commonly used to adjust spacing dynamically while rendering text in a PDF content stream.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_Tc(
        page: Page,
        source: Source,
        tc: float,
    ):
        Tc_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "Tc"]),
            None,
        )
        assert Tc_operator is not None
        Tc_operator.apply(
            operands=[tc],
            page=page,
            source=source,
        )

    @staticmethod
    def __apply_Tw(page: Page, source: Source, tw: float):
        Tw_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "Tw"]),
            None,
        )
        assert Tw_operator is not None
        Tw_operator.apply(
            operands=[tw],
            page=page,
            source=source,
        )

    @staticmethod
    def __apply_single_quote(page: Page, source: Source, text_to_render: str):
        single_quote_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "'"]),
            None,
        )
        assert single_quote_operator is not None
        single_quote_operator.apply(
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
        assert isinstance(operands[0], float) or isinstance(operands[0], int)
        assert isinstance(operands[1], float) or isinstance(operands[1], int)
        assert isinstance(operands[2], str) or isinstance(operands[2], hexstr)
        OperatorDoubleQuote.__apply_Tw(page=page, source=source, tw=operands[0])
        OperatorDoubleQuote.__apply_Tc(page=page, source=source, tc=operands[1])
        OperatorDoubleQuote.__apply_single_quote(
            page=page, source=source, text_to_render=operands[2]
        )

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return '"'

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 3
