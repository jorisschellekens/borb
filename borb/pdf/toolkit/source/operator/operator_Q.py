#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'Q' operator: Restore the graphics state.

This operator is used to restore the graphics state by removing the most recently saved
state from the graphics state stack and making it the current state. It effectively undoes
any changes made to the graphics state since the last 'q' operator was executed.

The graphics state includes various parameters such as the current transformation matrix,
the current color, line width, line cap style, and other drawing parameters. By using 'Q',
the system reverts to the state that was in effect at the time of the last 'q' operation,
ensuring that any changes made since that point are undone.

This operator is part of the graphics state stack mechanism, allowing for the temporary
modification of the graphics state during drawing operations, with the ability to revert to
a prior state when necessary.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
)


class OperatorQ(Operator):
    """
    The 'Q' operator: Restore the graphics state.

    This operator is used to restore the graphics state by removing the most recently saved
    state from the graphics state stack and making it the current state. It effectively undoes
    any changes made to the graphics state since the last 'q' operator was executed.

    The graphics state includes various parameters such as the current transformation matrix,
    the current color, line width, line cap style, and other drawing parameters. By using 'Q',
    the system reverts to the state that was in effect at the time of the last 'q' operation,
    ensuring that any changes made since that point are undone.

    This operator is part of the graphics state stack mechanism, allowing for the temporary
    modification of the graphics state during drawing operations, with the ability to revert to
    a prior state when necessary.
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
        # fmt: off
        graphics_state = source.graphics_state_stack[-1]
        source.graphics_state_stack.pop(-1)
        source.character_spacing = graphics_state["character_spacing"]
        source.flatness_tolerance = graphics_state["flatness_tolerance"]
        source.leading = graphics_state["leading"]
        source.line_cap_style = graphics_state["line_cap_style"]
        source.line_join_style = graphics_state["line_join_style"]
        source.miter_limit = graphics_state["miter_limit"]
        source.stroke_color = graphics_state["stroke_color"]
        source.stroke_color_space = graphics_state["stroke_color_space"]
        source.text_line_matrix = graphics_state["text_line_matrix"]
        source.text_matrix = graphics_state["text_matrix"]
        source.transformation_matrix = graphics_state["transformation_matrix"]
        pass
        # fmt: on

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "Q"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 0
