import copy
import typing
from decimal import Decimal

from ptext.io.read_transform.types import String
from ptext.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from ptext.pdf.canvas.event.event_listener import Event
from ptext.pdf.canvas.font.glyph_line import GlyphLine
from ptext.pdf.canvas.geometry.line_segment import LineSegment


class TextRenderEvent(Event):
    """
    This implementation of Event is triggered right after the Canvas has processed a text-rendering instruction
    """

    def __init__(self, graphics_state: CanvasGraphicsState, raw_bytes: String):
        self.graphics_state = graphics_state
        self.raw_bytes = raw_bytes
        self.glyph_line = graphics_state.font.build_glyph_line(raw_bytes)
        self.text_to_user_space_transform_matrix = graphics_state.text_matrix.mul(
            graphics_state.ctm
        )

        # store font family
        self.font_family = graphics_state.font.get_font_name()
        self.font_ascent = graphics_state.font.get_ascent()

        # store font size
        self.font_size = graphics_state.font_size

        # store font color
        self.font_color = graphics_state.non_stroke_color

        # store char spacing
        self.character_spacing = graphics_state.character_spacing

        # store space character width
        self.space_character_width = (
            graphics_state.font.get_space_character_width_estimate()
            * Decimal(0.001)
            * graphics_state.font_size
            * graphics_state.horizontal_scaling
            * Decimal(0.01)
        )

        # calculate baseline
        self.baseline = self._get_baseline(graphics_state)
        if raw_bytes != " ":
            bl = self.baseline

    def split_on_glyphs(self) -> typing.List["TextRenderEvent"]:
        split_events = []
        y: Decimal = self.get_baseline().y0
        x0: Decimal = min(self.get_baseline().x0, self.get_baseline().x1)
        x1: Decimal = x0
        for g in self.glyph_line.glyphs:
            e = TextRenderEvent(self.graphics_state, String(" "))
            e.glyph_line = GlyphLine([g])
            e.text_to_user_space_transform_matrix = copy.deepcopy(
                self.text_to_user_space_transform_matrix
            )
            e.font_size = self.font_size
            e.font_color = self.font_color
            e.font_family = self.font_family
            e.font_ascent = self.font_ascent
            e.space_character_width = self.space_character_width

            # calculate end of LineSegment
            x1 = x0 + (g.width / Decimal(1000)) * e.font_size

            # set LineSegment
            e.baseline = LineSegment(x0=x0, y0=y, x1=x1, y1=y)

            # append
            split_events.append(e)

            # prepare for next iteration
            x0 = x1

        return split_events

    def get_font_ascent(self) -> Decimal:
        return self.font_ascent

    def get_font_color(self):
        return self.font_color

    def get_font_family(self) -> str:
        return self.font_family

    def get_font_size(self) -> Decimal:
        return self.font_size

    def get_text(self) -> str:
        return self.glyph_line.get_text()

    def _get_baseline(self, graphics_state: CanvasGraphicsState) -> LineSegment:
        # build and transform line segment
        return LineSegment(
            Decimal(0),
            graphics_state.text_rise,
            self._get_pdf_string_width_in_text_space(graphics_state) or Decimal(0),
            graphics_state.text_rise,
        ).transform_by(self.text_to_user_space_transform_matrix)

    def get_baseline(self):
        return self.baseline

    def get_space_character_width_in_text_space(self):
        return self.space_character_width

    def _get_pdf_string_width_in_text_space(
        self, graphics_state: CanvasGraphicsState
    ) -> Decimal:
        """
        Get the width of a String in text space units
        """
        total_width = Decimal(0)
        for g in self.glyph_line:
            character_width = (
                Decimal(g.width) * Decimal(graphics_state.font_size) * Decimal(0.001)
            )

            # add word spacing where applicable
            if g.unicode == " ":
                character_width += Decimal(graphics_state.word_spacing)

            # horizontal scaling
            character_width *= Decimal(graphics_state.horizontal_scaling / 100)

            # add character spacing to character_width
            character_width += graphics_state.character_spacing

            # add character width to total
            total_width += character_width

        # subtract character spacing once (there are only N-1 spacings in a string of N characters)
        total_width -= Decimal(graphics_state.character_spacing)

        # return
        return total_width


class LeftToRightComparator:
    @staticmethod
    def cmp(obj0: TextRenderEvent, obj1: TextRenderEvent):

        # get baseline
        y0_round = obj0.get_baseline().y0
        y0_round = y0_round - y0_round % 5

        # get baseline
        y1_round = obj1.get_baseline().y0
        y1_round = y1_round - y1_round % 5

        if y0_round == y1_round:
            return obj0.get_baseline().x0 - obj1.get_baseline().x0
        return -(y0_round - y1_round)
