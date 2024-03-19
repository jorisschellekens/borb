#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered right after the Canvas has processed a text-rendering instruction
"""
import typing
from decimal import Decimal

from borb.io.read.types import String
from borb.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.glyph_line import GlyphLine
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText


class ChunkOfTextRenderEvent(Event, ChunkOfText):
    """
    This implementation of Event is triggered right after the Canvas has processed a text-rendering instruction
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, graphics_state: CanvasGraphicsState, raw_bytes: String):
        assert graphics_state.font is not None
        assert isinstance(graphics_state.font, Font)
        self._glyph_line: GlyphLine = GlyphLine.from_bytes(
            raw_bytes.get_value_bytes(),
            graphics_state.font,
            graphics_state.font_size,
            graphics_state.character_spacing,
            graphics_state.word_spacing,
            graphics_state.horizontal_scaling,
        )
        super(ChunkOfTextRenderEvent, self).__init__(
            font=graphics_state.font,
            font_color=graphics_state.non_stroke_color,
            font_size=graphics_state.font_size * graphics_state.text_matrix[1][1],
            text=self._glyph_line.get_text(),
        )
        m = graphics_state.text_matrix.mul(graphics_state.ctm)
        m[1][1] *= graphics_state.font_size

        # calculate baseline box
        p0 = m.cross(Decimal(0), graphics_state.text_rise, Decimal(1))
        p1 = m.cross(
            self._glyph_line.get_width_in_text_space(),
            graphics_state.text_rise
            + graphics_state.font.get_ascent() * Decimal(0.001),
            Decimal(1),
        )

        # set baseline box
        self._baseline_bounding_box = Rectangle(
            min(p0[0], p1[0]), min(p0[1], p1[1]), abs(p1[0] - p0[0]), abs(p1[1] - p0[1])
        )

        # calculate bounding box
        uses_descent = any(
            [x in self._text.lower() for x in ["y", "p", "q", "f", "g", "j"]]
        )
        if uses_descent:
            p0 = m.cross(
                Decimal(0),
                graphics_state.text_rise
                + graphics_state.font.get_descent() * Decimal(0.001),
                Decimal(1),
            )
            p1 = m.cross(
                self._glyph_line.get_width_in_text_space(),
                graphics_state.text_rise
                + graphics_state.font.get_ascent() * Decimal(0.001),
                Decimal(1),
            )
            self._previous_layout_box = Rectangle(
                min(p0[0], p1[0]),
                min(p0[1], p1[1]),
                abs(p1[0] - p0[0]),
                abs(p1[1] - p0[1]),
            )
        else:
            self._previous_layout_box = self._baseline_bounding_box

        # calculate space character width estimate
        current_font: Font = graphics_state.font
        self._space_character_width_estimate_in_user_space = (
            current_font.get_space_character_width_estimate()
            * graphics_state.font_size
            * graphics_state.text_matrix[0][0]
            * Decimal(0.001)
        )
        assert graphics_state.font_size is not None
        self._font_size: Decimal = (
            graphics_state.font_size * graphics_state.text_matrix[0][0]
        )

        # store graphics state
        self._graphics_state = graphics_state

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_baseline(self) -> Rectangle:
        """
        This function returns the bounding box of this ChunkOfTextRenderEvent,
        starting at the baseline (not at the descent)
        :return:    the baseline bounding box of this ChunkOfTextRenderEvent
        """
        return self._baseline_bounding_box

    def get_font_size(self) -> Decimal:
        """
        This function returns the font size of this ChunkOfTextRenderEvent,
        :return:    the font size of this ChunkOfTextRenderEvent
        """
        return self._font_size

    def get_space_character_width_estimate_in_text_space(self) -> Decimal:
        """
        This function returns the width (in text space) of the space-character.
        :return:    the space character width of this ChunkOfTextRenderEvent
        """
        return (
            self._space_character_width_estimate_in_user_space
            * Decimal(1000)
            / self._font_size
        )

    def get_space_character_width_estimate_in_user_space(self) -> Decimal:
        """
        This function returns the width (in user space) of the space-character.
        :return:    the space character width of this ChunkOfTextRenderEvent
        """
        return self._space_character_width_estimate_in_user_space

    def split_on_glyphs(self) -> typing.List["ChunkOfTextRenderEvent"]:
        """
        This function splits this ChunkOfTextRenderEvent on every Glyph
        :return:    this ChunkOfTextRenderEvent, split on glyphs (as a typing.List[ChunkOfTextRenderEvent])
        """
        chunks_of_text: typing.List[ChunkOfTextRenderEvent] = []
        x: Decimal = Decimal(0)
        y: Decimal = self._graphics_state.text_rise
        assert isinstance(self._graphics_state.font, Font)
        assert self._graphics_state.font is not None
        font: Font = self._graphics_state.font
        for g in self._glyph_line.split():
            e = ChunkOfTextRenderEvent(self._graphics_state, String(" "))
            e._font_size = self._font_size
            e._font_color = self._font_color
            e._font = self._font
            e._text = g.get_text()
            e._space_character_width_estimate_in_user_space = (
                self._space_character_width_estimate_in_user_space
            )
            e._graphics_state = self._graphics_state
            e._glyph_line = g

            # set baseline bounding box
            m = self._graphics_state.text_matrix.mul(self._graphics_state.ctm)
            m[1][1] *= self._graphics_state.font_size
            p0 = m.cross(x, y, Decimal(1))
            p1 = m.cross(
                x + g.get_width_in_text_space(),
                y + font.get_ascent() * Decimal(0.001),
                Decimal(1),
            )
            e._baseline_bounding_box = Rectangle(
                p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1]
            )
            e._previous_layout_box = e._baseline_bounding_box

            # change bounding box (descent)
            if g.uses_descent():
                p0 = m.cross(
                    x,
                    y + font.get_descent() * Decimal(0.001),
                    Decimal(1),
                )
                p1 = m.cross(
                    x + g.get_width_in_text_space(),
                    y + font.get_ascent() * Decimal(0.001),
                    Decimal(1),
                )
                e._previous_layout_box = Rectangle(
                    min(p0[0], p1[0]),
                    min(p0[1], p1[1]),
                    abs(p1[0] - p0[0]),
                    abs(p1[1] - p0[1]),
                )

            # update x
            x += g.get_width_in_text_space()

            # append
            chunks_of_text.append(e)

        return chunks_of_text


class LeftToRightComparator:
    """
    This class offers a comparator on ChunkOfTextRenderEvent objects.
    This comparator favors left-to-right, up-to-down text reading order.
    This corresponds to the expected western language reading order.
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

    @staticmethod
    def cmp(obj0: ChunkOfTextRenderEvent, obj1: ChunkOfTextRenderEvent):
        """
        This function compares two ChunkOfTextRenderEvent objects
        returning a negative number if obj0 occurs first in the (western) reading order,
        and a positive number otherwise.
        :param obj0:    the first ChunkOfTextRenderEvent
        :param obj1:    the second ChunkOfTextRenderEvent
        :return:        a negative number if obj0 occurs first (in left-to-right, top-to-bottom reading), positive otherwise
        """
        # get baseline
        y0_round = obj0.get_baseline().y
        y0_round = y0_round - y0_round % 5

        # get baseline
        y1_round = obj1.get_baseline().y
        y1_round = y1_round - y1_round % 5

        if y0_round == y1_round:
            return obj0.get_baseline().x - obj1.get_baseline().x
        return -(y0_round - y1_round)
