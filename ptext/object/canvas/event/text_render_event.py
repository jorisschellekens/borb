from typing import Optional

from ptext.object.canvas.geometry.line_segment import LineSegment
from ptext.object.pdf_high_level_object import Event
from ptext.primitive.pdf_string import PDFString, PDFHexString, PDFLiteralString


class TextRenderEvent(Event):
    def __init__(self, graphics_state: "CanvasGraphicsState", text: "PDFString"):
        self.text = text
        self.text_to_user_space_transform_matrix = graphics_state.text_matrix.mul(
            graphics_state.ctm
        )

        # store font family
        self.font_family = graphics_state.font.get_font_name()

        # store font size
        self.font_size = graphics_state.font_size

        # store font color
        self.font_color = graphics_state.non_stroke_color

        # store char spacing
        self.character_spacing = graphics_state.character_spacing

        # store average character width
        self.avg_character_width_in_text_space = (
            self._calculate_avg_character_width_in_text_space(graphics_state)
        )
        # calculate baseline
        self.baseline = self._calculate_baseline(graphics_state)

        # store space-character width
        self.space_character_width_in_text_space = (
            self._calculate_space_character_width_in_text_space(graphics_state)
        )

    def get_avg_character_width_in_text_space(self):
        return self.avg_character_width_in_text_space

    def get_font_color(self):
        return self.font_color

    def get_font_family(self):
        return self.font_family

    def get_font_size(self):
        return self.font_size

    def get_space_character_width_in_text_space(self):
        return self.space_character_width_in_text_space

    def get_text(self) -> str:
        return (
            self.text.get_text()
            if isinstance(self.text, PDFLiteralString)
            else self.text.get_decoded_text()
        )

    def _calculate_avg_character_width_in_text_space(
        self, graphics_state: "CanvasGraphicsState"
    ) -> float:
        cw = graphics_state.font.get_average_character_width()
        if cw is None:
            txt = self.get_text()
            cw = (
                graphics_state.font.get_width(PDFLiteralString(txt)) / len(txt)
                if len(txt) > 0
                else 0
            )
        # relative size
        cw *= 0.001
        # take into account font size
        cw *= graphics_state.font_size
        # take into account font matrix
        cw *= graphics_state.horizontal_scaling / 100
        # return
        return cw

    def _calculate_baseline(self, graphics_state: "CanvasGraphicsState") -> LineSegment:
        # build and transform line segment
        return LineSegment(
            0,
            graphics_state.text_rise,
            self._get_pdf_string_width_in_text_space(self.text, graphics_state),
            graphics_state.text_rise,
        ).transform_by(self.text_to_user_space_transform_matrix)

    def _calculate_space_character_width_in_text_space(
        self, graphics_state: "CanvasGraphicsState"
    ) -> Optional[float]:
        """
        Gets the width of the space character in text space units
        """
        cw = self._get_pdf_string_width_in_text_space(PDFString(" "), graphics_state)
        if cw is not None:
            return cw
        if cw == 0:
            cw = graphics_state.font.get_avg_character_width_in_text_space()
            if cw is None:
                return None
            cw *= graphics_state.font_size
            cw *= 0.001
            cw += graphics_state.character_spacing
            cw += graphics_state.word_spacing
            cw *= graphics_state.horizontal_scaling / 100
        # return
        return cw

    def get_baseline(self):
        return self.baseline

    def _get_pdf_string_width_in_text_space(
        self, text: "PDFString", graphics_state: "CanvasGraphicsState"
    ) -> float:
        """
        Get the width of a PDFString in text space units
        """
        underlying_text = (
            text.get_decoded_text()
            if isinstance(text, PDFHexString)
            else text.get_text()
        )
        if len(underlying_text) == 1:
            o = (
                graphics_state.font.get_width(PDFString(underlying_text[0:1]))
                * graphics_state.font_size
                * 0.001
            )
            # character spacing
            o += graphics_state.character_spacing
            # word spacing if we are rendering a <space>
            o += graphics_state.word_spacing if underlying_text == " " else 0
            # apply horizontal scaling
            o *= graphics_state.horizontal_scaling / 100
            return o
        else:
            sum = 0
            for i in range(0, len(underlying_text)):
                sum += self._get_pdf_string_width_in_text_space(
                    PDFString(underlying_text[i : i + 1]), graphics_state
                )
            sum -= graphics_state.character_spacing
            return sum


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
