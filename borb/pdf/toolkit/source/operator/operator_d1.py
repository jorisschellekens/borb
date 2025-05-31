#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'd1' operator: Set width and bounding box information for the glyph and declare that the glyph description specifies only shape, not colour.

The 'd1' operator is used in Type 3 fonts within a PDF content stream to define the width and bounding box of a glyph,
and to indicate that the glyph description specifies only the shape of the glyph, not its colour. Specifically, the
operator sets the horizontal displacement (wx) of the glyph in the glyph coordinate system, which must be consistent
with the corresponding width in the font's Widths array, while the vertical displacement (wy) is set to 0.

In addition to width information, this operator also defines the bounding box for the glyph, specified by the lower-left
corner (llx, lly) and the upper-right corner (urx, ury). This bounding box should be large enough to enclose the entire
glyph, including any marks that result from executing the glyph's description. If the bounding box is too small and marks
fall outside of it, the result is unpredictable.

This operator is used when the glyph's colour is determined by the graphics state and not specified within the glyph's
description. As such, the glyph description should not execute any operators that set colour or colour-related parameters;
any such operators will be ignored. Additionally, the glyph description should not include an image, though an image mask
is acceptable.

This operator must only be used in a content stream found in a Type 3 font's CharProcs dictionary.

Note:
    - The 'd1' operator name ends with the digit '1', distinguishing it from the 'd0' operator.
    - The bounding box must be large enough to fully enclose the glyph. If marks fall outside this box, the result is unpredictable.
    - For more details on glyph positioning and metrics, refer to PDF specification section 9.2.4, "Glyph Positioning and Metrics."
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatord1(Operator):
    """
    The 'd1' operator: Set width and bounding box information for the glyph and declare that the glyph description specifies only shape, not colour.

    The 'd1' operator is used in Type 3 fonts within a PDF content stream to define the width and bounding box of a glyph,
    and to indicate that the glyph description specifies only the shape of the glyph, not its colour. Specifically, the
    operator sets the horizontal displacement (wx) of the glyph in the glyph coordinate system, which must be consistent
    with the corresponding width in the font's Widths array, while the vertical displacement (wy) is set to 0.

    In addition to width information, this operator also defines the bounding box for the glyph, specified by the lower-left
    corner (llx, lly) and the upper-right corner (urx, ury). This bounding box should be large enough to enclose the entire
    glyph, including any marks that result from executing the glyph's description. If the bounding box is too small and marks
    fall outside of it, the result is unpredictable.

    This operator is used when the glyph's colour is determined by the graphics state and not specified within the glyph's
    description. As such, the glyph description should not execute any operators that set colour or colour-related parameters;
    any such operators will be ignored. Additionally, the glyph description should not include an image, though an image mask
    is acceptable.

    This operator must only be used in a content stream found in a Type 3 font's CharProcs dictionary.

    Note:
        - The 'd1' operator name ends with the digit '1', distinguishing it from the 'd0' operator.
        - The bounding box must be large enough to fully enclose the glyph. If marks fall outside this box, the result is unpredictable.
        - For more details on glyph positioning and metrics, refer to PDF specification section 9.2.4, "Glyph Positioning and Metrics."
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
        assert isinstance(operands[4], float) or isinstance(operands[4], int)
        assert isinstance(operands[5], float) or isinstance(operands[5], int)
        wx: typing.Union[float, int] = operands[0]
        wy: typing.Union[float, int] = operands[1]
        llx: typing.Union[float, int] = operands[2]
        lly: typing.Union[float, int] = operands[3]
        urx: typing.Union[float, int] = operands[4]
        ury: typing.Union[float, int] = operands[5]
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "d1"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 6
