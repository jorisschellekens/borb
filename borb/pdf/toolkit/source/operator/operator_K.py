#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'K' operator: Set the stroking color space to DeviceCMYK and set the color for stroking operations.

This operator sets the color space for stroking operations to DeviceCMYK (or DefaultCMYK).
The four operands represent the CMYK components of the color, where each value is between 0.0 (zero concentration)
and 1.0 (maximum concentration). The four operands correspond to:

- C: Cyan
- M: Magenta
- Y: Yellow
- K: Black (Key)

The behavior of this operator is also influenced by the current overprint mode (see section 8.6.7, "Overprint Control").

This operator ensures that the specified color is used for stroking paths in the PDF content stream, affecting how paths are
painted with the given CMYK color.

See PDF specification section 8.6.5.6, "Default Color Spaces" for more details.
"""

import typing

from borb.pdf.color.cmyk_color import CMYKColor
from borb.pdf.page import Page
from borb.pdf.primitives import PDFType, name
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorK(Operator):
    """
    The 'K' operator: Set the stroking color space to DeviceCMYK and set the color for stroking operations.

    This operator sets the color space for stroking operations to DeviceCMYK (or DefaultCMYK).
    The four operands represent the CMYK components of the color, where each value is between 0.0 (zero concentration)
    and 1.0 (maximum concentration). The four operands correspond to:

    - C: Cyan
    - M: Magenta
    - Y: Yellow
    - K: Black (Key)

    The behavior of this operator is also influenced by the current overprint mode (see section 8.6.7, "Overprint Control").

    This operator ensures that the specified color is used for stroking paths in the PDF content stream, affecting how paths are
    painted with the given CMYK color.

    See PDF specification section 8.6.5.6, "Default Color Spaces" for more details.
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
        cyan: typing.Union[float, int] = operands[0]
        magenta: typing.Union[float, int] = operands[1]
        yellow: typing.Union[float, int] = operands[2]
        key: typing.Union[float, int] = operands[3]
        source.stroke_color_space = name("DeviceCMYK")
        source.stroke_color = CMYKColor(
            cyan=cyan, magenta=magenta, yellow=yellow, key=key
        )
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "K"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 4
