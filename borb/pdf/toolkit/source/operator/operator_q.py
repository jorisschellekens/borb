#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'q' operator: Save the current graphics state.

This operator is used to save the current graphics state onto the graphics state stack.
It effectively preserves all parameters of the current graphics state, including the
current transformation matrix, colors, line width, and other drawing attributes.

After executing 'q', any subsequent changes to the graphics state (such as transformations,
color changes, etc.) do not affect the saved state. The state can later be restored with
the 'Q' operator, which pops the most recently saved state from the stack and makes it
the current state.

The 'q' operator is useful for temporarily altering the graphics state during drawing
operations, with the ability to revert back to the saved state when needed, allowing for
more flexible drawing control.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class Operatorq(Operator):
    """
    The 'q' operator: Save the current graphics state.

    This operator is used to save the current graphics state onto the graphics state stack.
    It effectively preserves all parameters of the current graphics state, including the
    current transformation matrix, colors, line width, and other drawing attributes.

    After executing 'q', any subsequent changes to the graphics state (such as transformations,
    color changes, etc.) do not affect the saved state. The state can later be restored with
    the 'Q' operator, which pops the most recently saved state from the stack and makes it
    the current state.

    The 'q' operator is useful for temporarily altering the graphics state during drawing
    operations, with the ability to revert back to the saved state when needed, allowing for
    more flexible drawing control.
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
        import copy

        source.graphics_state_stack += [
            {
                "character_spacing": source.character_spacing,
                "flatness_tolerance": source.flatness_tolerance,
                "leading": source.leading,
                "line_cap_style": source.line_cap_style,
                "line_join_style": source.line_join_style,
                "miter_limit": source.miter_limit,
                "stroke_color": source.stroke_color,
                "stroke_color_space": source.stroke_color_space,
                "text_line_matrix": copy.deepcopy(source.text_line_matrix),
                "text_matrix": copy.deepcopy(source.text_matrix),
                "transformation_matrix": copy.deepcopy(source.transformation_matrix),
            }
        ]
        pass

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "q"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
