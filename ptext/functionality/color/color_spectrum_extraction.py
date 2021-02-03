import typing
from typing import Optional

from ptext.io.read_transform.types import Decimal
from ptext.pdf.canvas.color.color import RGBColor
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.event.text_render_event import TextRenderEvent
from ptext.pdf.page.page import Page


class ColorSpectrumExtraction(EventListener):
    """
    This implementation of EventListener  extracts the colors used in rendering a PDF
    """

    def __init__(self, maximum_number_of_colors: Optional[int] = None):
        """
        Constructs a new ColorSpectrumExtraction
        """
        self.maximum_number_of_colors = 64
        if maximum_number_of_colors is not None:
            self.maximum_number_of_colors = maximum_number_of_colors
        self.colors_per_page: typing.Dict[
            int, typing.Dict[typing.Tuple[int, int, int], int]
        ] = {}
        self.current_page = -1

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, TextRenderEvent):
            self._render_text(event)
        if isinstance(event, ImageRenderEvent):
            self._render_image(event)

    def _begin_page(self, page: Page):
        self.current_page += 1
        self.colors_per_page[self.current_page] = {}

    def _render_text(self, event: TextRenderEvent):
        assert event is not None
        w = event.get_baseline().length()
        h = event.get_font_size()
        c = event.get_font_color()
        self._register_color(w * h, c)

    def _render_image(self, event: ImageRenderEvent):
        w = event.get_width()
        h = event.get_height()
        for i in range(0, int(w)):
            for j in range(0, int(h)):
                self._register_color(1, event.get_rgb(i, j))

    def _register_color(self, amount: int, color: RGBColor):
        mod_step = int(256 / (self.maximum_number_of_colors ** (1.0 / 3)))
        r = int(color.to_rgb().red)
        r = r - r % mod_step

        g = int(color.to_rgb().green)
        g = g - g % mod_step

        b = int(color.to_rgb().blue)
        b = b - b % mod_step

        t = (r, g, b)
        if t not in self.colors_per_page[self.current_page]:
            self.colors_per_page[self.current_page][t] = amount
        else:
            self.colors_per_page[self.current_page][t] += amount

    def get_colors_per_page(self, page_number: int, limit: Optional[int] = None):
        if limit is None:
            limit = 32
        tmp = sorted(
            [
                (RGBColor(Decimal(k[0]), Decimal(k[1]), Decimal(k[2])), int(v))
                for k, v in self.colors_per_page[page_number].items()
            ],
            key=lambda x: x[1],
        )[-limit:]
        return tmp
