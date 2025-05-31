#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Tf' operator: Set the text font and size.

This operator sets the font and size for subsequent text operations. The operand
for this operator is a font name (which must be defined in the current resource
dictionary) and a size in text space units.

The font is specified by a name object, which corresponds to an entry in the
Font subdictionary of the current resource dictionary. The size is specified as
a number, which represents the size of the text in unscaled text space units.

After this operator is executed, all subsequent text drawing operators will use
this font and size until another 'Tf' operator is encountered.

Note:
    - The font name must refer to a font in the current resource dictionary.
    - The size is expressed in unscaled text space units, and it is used to scale
      text characters when drawing text.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTf(Operator):
    """
    The 'Tf' operator: Set the text font and size.

    This operator sets the font and size for subsequent text operations. The operand
    for this operator is a font name (which must be defined in the current resource
    dictionary) and a size in text space units.

    The font is specified by a name object, which corresponds to an entry in the
    Font subdictionary of the current resource dictionary. The size is specified as
    a number, which represents the size of the text in unscaled text space units.

    After this operator is executed, all subsequent text drawing operators will use
    this font and size until another 'Tf' operator is encountered.

    Note:
        - The font name must refer to a font in the current resource dictionary.
        - The size is expressed in unscaled text space units, and it is used to scale
          text characters when drawing text.
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
        assert isinstance(operands[0], name)
        assert isinstance(operands[1], float) or isinstance(operands[1], int)
        source.font = (
            page.get("Resources", {}).get("Font", {}).get(operands[0][1:], None)
        )
        source.font_size = operands[1]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Tf"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 2
