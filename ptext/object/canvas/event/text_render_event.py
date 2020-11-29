from decimal import Decimal

from ptext.object.canvas.geometry.line_segment import LineSegment
from ptext.object.event_listener import Event
from ptext.primitive.pdf_string import PDFString, PDFHexString, PDFLiteralString


class TextRenderEvent(Event):
    """
    This implementation of Event is triggered right after the Canvas has processed a text-rendering instruction
    """

    def __init__(self, graphics_state: "CanvasGraphicsState", raw_bytes: "PDFString"):
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

    def _get_baseline(self, graphics_state: "CanvasGraphicsState") -> LineSegment:
        # build and transform line segment
        return LineSegment(
            Decimal(0),
            graphics_state.text_rise,
            self._get_pdf_string_width_in_text_space(self.raw_bytes, graphics_state)
            or Decimal(0),
            graphics_state.text_rise,
        ).transform_by(self.text_to_user_space_transform_matrix)

    def get_baseline(self):
        return self.baseline

    def get_space_character_width_in_text_space(self):
        return self.space_character_width

    def _get_pdf_string_width_in_text_space(
        self, text: "PDFString", graphics_state: "CanvasGraphicsState"
    ) -> Decimal:
        """
        Get the width of a PDFString in text space units
        """
        if isinstance(text, PDFLiteralString):
            w = Decimal(0)
            for g in self.glyph_line:
                character_width = (
                    Decimal(g.width)
                    * Decimal(graphics_state.font_size)
                    * Decimal(0.001)
                )
                if g.unicode == " ":
                    character_width += Decimal(graphics_state.word_spacing)
                character_width *= Decimal(graphics_state.horizontal_scaling / 100)
                w += character_width
            w -= Decimal(graphics_state.character_spacing)
            return w

        if isinstance(text, PDFHexString):
            pass


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
