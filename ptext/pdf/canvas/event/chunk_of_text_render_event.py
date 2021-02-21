#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of Event is triggered right after the Canvas has processed a text-rendering instruction
"""
import typing
from decimal import Decimal

from ptext.io.read.types import String
from ptext.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from ptext.pdf.canvas.event.event_listener import Event
from ptext.pdf.canvas.font.glyph_line import GlyphLine
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import ChunkOfText


class ChunkOfTextRenderEvent(Event, ChunkOfText):
    """
    This implementation of Event is triggered right after the Canvas has processed a text-rendering instruction
    """

    def __init__(self, graphics_state: CanvasGraphicsState, raw_bytes: String):
        self._glyph_line: GlyphLine = graphics_state.font.build_glyph_line(raw_bytes)
        super(ChunkOfTextRenderEvent, self).__init__(
            font=graphics_state.font,
            font_size=graphics_state.font_size,
            font_color=graphics_state.non_stroke_color,
            text=self._glyph_line.get_text(),
        )
        m = graphics_state.text_matrix.mul(graphics_state.ctm)

        # calculate baseline box
        p0 = m.cross(0, graphics_state.text_rise, Decimal(1))
        p1 = m.cross(
            self._glyph_line.get_width_in_text_space(
                graphics_state.font_size,
                graphics_state.character_spacing,
                graphics_state.word_spacing,
                graphics_state.horizontal_scaling,
            ),
            graphics_state.text_rise
            + graphics_state.font.get_ascent() * Decimal(0.001),
            Decimal(1),
        )
        # set baseline box
        self.baseline_bounding_box = Rectangle(
            min(p0[0], p1[0]), min(p0[1], p1[1]), abs(p1[0] - p0[0]), abs(p1[1] - p0[1])
        )

        # calculate bounding box
        uses_descent = any(
            [x in self.text.lower() for x in ["y", "p", "q", "f", "g", "j"]]
        )
        if uses_descent:
            p0 = m.cross(
                0,
                graphics_state.text_rise
                + graphics_state.font.get_descent() * Decimal(0.001),
                Decimal(1),
            )
            p1 = m.cross(
                self._glyph_line.get_width_in_text_space(
                    graphics_state.font_size,
                    graphics_state.character_spacing,
                    graphics_state.word_spacing,
                    graphics_state.horizontal_scaling,
                ),
                graphics_state.text_rise
                + graphics_state.font.get_ascent() * Decimal(0.001),
                Decimal(1),
            )
            self.set_bounding_box(
                Rectangle(
                    min(p0[0], p1[0]),
                    min(p0[1], p1[1]),
                    abs(p1[0] - p0[0]),
                    abs(p1[1] - p0[1]),
                )
            )
        else:
            self.set_bounding_box(self.baseline_bounding_box)

        # calculate space character width estimate
        self.space_character_width_estimate = (
            self.font.get_space_character_width_estimate()
            * Decimal(0.001)
            * self.font_size
            * graphics_state.horizontal_scaling
            * Decimal(0.01)
        )

        # store graphics state
        self._graphics_state = graphics_state

    def get_space_character_width_estimate(self):
        return self.space_character_width_estimate

    def get_baseline(self) -> Rectangle:
        return self.baseline_bounding_box

    def split_on_glyphs(self) -> typing.List["ChunkOfTextRenderEvent"]:
        chunks_of_text: typing.List[ChunkOfTextRenderEvent] = []
        x: Decimal = Decimal(0)
        y: Decimal = self._graphics_state.text_rise
        for g in self._glyph_line.glyphs:
            e = ChunkOfTextRenderEvent(self._graphics_state, String(" "))
            e.font_size = self.font_size
            e.font_color = self.font_color
            e.font = self.font
            e.text = chr(g.unicode)
            e.space_character_width_estimate = self.space_character_width_estimate
            e._graphics_state = self._graphics_state
            e._glyph_line = GlyphLine([g])
            # calculate width
            width: Decimal = (
                g.width
                * Decimal(0.001)
                * self.font_size
                * self._graphics_state.horizontal_scaling
                * Decimal(0.01)
                + (
                    self._graphics_state.word_spacing
                    if chr(g.unicode) == " "
                    else Decimal(0)
                )
                + self._graphics_state.character_spacing
            )

            # set baseline bounding box
            m = self._graphics_state.text_matrix.mul(self._graphics_state.ctm)
            p0 = m.cross(x, y, Decimal(1))
            p1 = m.cross(
                x + width,
                y + self._graphics_state.font.get_ascent() * Decimal(0.001),
                Decimal(1),
            )
            e.baseline_bounding_box = Rectangle(
                p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1]
            )
            e.bounding_box = e.baseline_bounding_box

            # change bounding box (descent)
            uses_descent = chr(g.unicode).lower() in ["y", "p", "q", "f", "g", "j"]
            if uses_descent:
                p0 = m.cross(
                    x,
                    y + self._graphics_state.font.get_descent() * Decimal(0.001),
                    Decimal(1),
                )
                p1 = m.cross(
                    x + width,
                    y + self._graphics_state.font.get_ascent() * Decimal(0.001),
                    Decimal(1),
                )
                e.bounding_box = Rectangle(
                    min(p0[0], p1[0]),
                    min(p0[1], p1[1]),
                    abs(p1[0] - p0[0]),
                    abs(p1[1] - p0[1]),
                )

            # update x
            x += width

            # append
            chunks_of_text.append(e)

        return chunks_of_text


class LeftToRightComparator:
    @staticmethod
    def cmp(obj0: ChunkOfTextRenderEvent, obj1: ChunkOfTextRenderEvent):

        # get baseline
        y0_round = obj0.get_baseline().y
        y0_round = y0_round - y0_round % 5

        # get baseline
        y1_round = obj1.get_baseline().y
        y1_round = y1_round - y1_round % 5

        if y0_round == y1_round:
            return obj0.get_baseline().x - obj1.get_baseline().x
        return -(y0_round - y1_round)
