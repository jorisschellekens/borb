#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Tr' operator: Set text rendering mode.

This operator sets the text rendering mode in the current graphics state, determining
how text is rendered. The rendering mode specifies whether the text is filled, stroked,
or both. It also controls whether the text is clipped.

The valid values for the rendering mode are:
    - 0: Fill text (default mode).
    - 1: Stroke text (outline the text).
    - 2: Fill and stroke text (both fill and outline the text).
    - 3: Fill text and add text clipping path.
    - 4: Stroke text and add text clipping path.
    - 5: Fill, stroke, and add text clipping path.

Note:
    - This operator affects only the rendering of text and does not affect other graphical elements.
    - The `Tr` operator is typically used to create effects such as outlining, filling, or clipping text
      based on its path.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorTr(Operator):
    """
    The 'Tr' operator: Set text rendering mode.

    This operator sets the text rendering mode in the current graphics state, determining
    how text is rendered. The rendering mode specifies whether the text is filled, stroked,
    or both. It also controls whether the text is clipped.

    The valid values for the rendering mode are:
        - 0: Fill text (default mode).
        - 1: Stroke text (outline the text).
        - 2: Fill and stroke text (both fill and outline the text).
        - 3: Fill text and add text clipping path.
        - 4: Stroke text and add text clipping path.
        - 5: Fill, stroke, and add text clipping path.

    Note:
        - This operator affects only the rendering of text and does not affect other graphical elements.
        - The `Tr` operator is typically used to create effects such as outlining, filling, or clipping text
          based on its path.
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
        # Set text rendering mode
        assert isinstance(operands[0], int)
        source.text_rendering_mode = operands[0]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Tr"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
