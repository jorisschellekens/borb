#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Tw' operator: Set word spacing.

This operator sets the word spacing parameter in the text state. Word spacing is added
to the advance width of the space character (defined in the font) during text layout.
This allows precise control over the spacing between words in a text string.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTw(Operator):
    """
    The 'Tw' operator: Set word spacing.

    This operator sets the word spacing parameter in the text state. Word spacing is added
    to the advance width of the space character (defined in the font) during text layout.
    This allows precise control over the spacing between words in a text string.
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
        source.word_spacing = operands[0]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Tw"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
