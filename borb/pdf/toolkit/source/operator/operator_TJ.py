#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'TJ' operator: Show one or more text strings, allowing individual glyph positioning.

This operator displays one or more text strings, with the option to adjust the
position of each string (or individual glyphs) relative to the previous one. The
operand for this operator is an array of strings and/or numbers. Each element of
the array can be either a string (representing the text to be displayed) or a number
(representing an adjustment to the current text position).

If the element is a string, it is shown at the current text position. If the element
is a number, the text position is adjusted by that amount. The number is expressed
in thousandths of a unit of text space, meaning the adjustment is made in text space units,
and the value is subtracted from the current coordinate depending on the writing mode.

The effect of a positive number is to move the next glyph either to the left (in horizontal writing mode)
or down (in vertical writing mode).

Example:
    - ['Hello ', 10, 'World'] would display the string 'Hello' at the current position,
      adjust the position by 10 units, and then display 'World' at the new position.

Note:
    - The operator allows fine control over glyph positioning within the text string.
    - The operands in the array are processed sequentially, applying any positional
      adjustments between the glyphs.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTJ(Operator):
    """
    The 'TJ' operator: Show one or more text strings, allowing individual glyph positioning.

    This operator displays one or more text strings, with the option to adjust the
    position of each string (or individual glyphs) relative to the previous one. The
    operand for this operator is an array of strings and/or numbers. Each element of
    the array can be either a string (representing the text to be displayed) or a number
    (representing an adjustment to the current text position).

    If the element is a string, it is shown at the current text position. If the element
    is a number, the text position is adjusted by that amount. The number is expressed
    in thousandths of a unit of text space, meaning the adjustment is made in text space units,
    and the value is subtracted from the current coordinate depending on the writing mode.

    The effect of a positive number is to move the next glyph either to the left (in horizontal writing mode)
    or down (in vertical writing mode).

    Example:
        - ['Hello ', 10, 'World'] would display the string 'Hello' at the current position,
          adjust the position by 10 units, and then display 'World' at the new position.

    Note:
        - The operator allows fine control over glyph positioning within the text string.
        - The operands in the array are processed sequentially, applying any positional
          adjustments between the glyphs.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __apply_Tj(page: Page, source: Source, text_to_render: str):
        Tj_operator: typing.Optional[Operator] = next(
            iter([x for x in source.operators if x.get_name() == "Tj"]),
            None,
        )
        assert Tj_operator is not None
        Tj_operator.apply(
            page=page,
            source=source,
            operands=[text_to_render],
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
        assert isinstance(operands[0], typing.List)
        array_to_render: typing.List = operands[0]
        for operand in array_to_render:
            if isinstance(operand, str):
                self.__apply_Tj(page=page, source=source, text_to_render=operand)
            if isinstance(operand, float) or isinstance(operand, int):
                source.text_matrix[2][0] += (
                    operand
                    * 0.001
                    * source.font_size
                    * (source.horizontal_scaling * 0.01)
                )
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "TJ"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
