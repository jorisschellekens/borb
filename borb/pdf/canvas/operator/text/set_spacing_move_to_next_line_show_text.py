#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Move to the next line and show a text string, using a w as the word spacing
and a c as the character spacing (setting the corresponding parameters in
the text state). a w and a c shall be numbers expressed in unscaled text
space units.
"""
import typing

from borb.io.read.types import AnyPDFType
from borb.pdf.canvas.operator.canvas_operator import CanvasOperator


class SetSpacingMoveToNextLineShowText(CanvasOperator):
    """
    Move to the next line and show a text string, using a w as the word spacing
    and a c as the character spacing (setting the corresponding parameters in
    the text state). a w and a c shall be numbers expressed in unscaled text
    space units. This operator shall have the same effect as this code:
    aw Tw
    ac Tc
    string '
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super().__init__('"', 3)

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def invoke(
        self,
        canvas_stream_processor: "CanvasStreamProcessor",  # type: ignore [name-defined]
        operands: typing.List[AnyPDFType] = [],
        event_listeners: typing.List["EventListener"] = [],  # type: ignore [name-defined]
    ) -> None:
        """
        Invoke the " operator
        :param canvas_stream_processor:     the CanvasStreamProcessor
        :param operands:                    the operands for this CanvasOperator
        :param event_listeners:             the typing.List of EventListener(s) that may be notified
        :return:                            None
        """
        set_word_spacing_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("Tw")
        assert (
            set_word_spacing_op
        ), 'Operator Tw must be defined for operator " to function'
        set_word_spacing_op.invoke(
            canvas_stream_processor, [operands[0]], event_listeners
        )

        set_character_spacing_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("Tc")
        assert (
            set_character_spacing_op
        ), 'Operator Tc must be defined for operator " to function'
        set_character_spacing_op.invoke(
            canvas_stream_processor, [operands[1]], event_listeners
        )

        move_to_next_line_show_text_op: typing.Optional[
            CanvasOperator
        ] = canvas_stream_processor.get_operator("'")
        assert (
            move_to_next_line_show_text_op
        ), "Operator ' must be defined for operator \" to function"
        move_to_next_line_show_text_op.invoke(
            canvas_stream_processor, [operands[2]], event_listeners
        )
