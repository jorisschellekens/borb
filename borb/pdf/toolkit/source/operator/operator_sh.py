#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'sh' operator: Paint the shape and color shading described by a shading dictionary.

This operator paints the shape and color shading described by a shading dictionary,
subject to the current clipping path. Unlike other operators, the current color in
the graphics state is neither used nor altered during this operation.

The operand 'name' refers to the name of a shading dictionary resource in the Shading
subdictionary of the current resource dictionary. All coordinates in the shading dictionary
are interpreted relative to the current user space. If used within a type 2 pattern, the
coordinates would be in pattern space instead. The colors in the shading dictionary are
interpreted in the color space identified by the dictionary’s `ColorSpace` entry, while the
`Background` entry, if present, is ignored.

Note:
    This operator should be applied only to bounded or geometrically defined shadings.
    If applied to an unbounded shading, the shading’s gradient fill will be painted across
    the entire clipping region, which could be time-consuming.

See also:
    - Shading dictionary (7.8.3, "Resource Dictionaries")
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorsh(Operator):
    """
    The 'sh' operator: Paint the shape and color shading described by a shading dictionary.

    This operator paints the shape and color shading described by a shading dictionary,
    subject to the current clipping path. Unlike other operators, the current color in
    the graphics state is neither used nor altered during this operation.

    The operand 'name' refers to the name of a shading dictionary resource in the Shading
    subdictionary of the current resource dictionary. All coordinates in the shading dictionary
    are interpreted relative to the current user space. If used within a type 2 pattern, the
    coordinates would be in pattern space instead. The colors in the shading dictionary are
    interpreted in the color space identified by the dictionary’s `ColorSpace` entry, while the
    `Background` entry, if present, is ignored.

    Note:
        This operator should be applied only to bounded or geometrically defined shadings.
        If applied to an unbounded shading, the shading’s gradient fill will be painted across
        the entire clipping region, which could be time-consuming.

    See also:
        - Shading dictionary (7.8.3, "Resource Dictionaries")
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
        # TODO
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "sh"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 1
