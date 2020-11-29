from decimal import Decimal
from typing import List

from ptext.object.canvas.event.text_render_event import TextRenderEvent
from ptext.object.canvas.geometry.line_segment import LineSegment
from ptext.object.canvas.geometry.rectangle import Rectangle


class LineRenderEvent(TextRenderEvent):
    def __init__(self, text_render_events: List[TextRenderEvent]):
        self.text_render_events = text_render_events

    def get_font_color(self):
        return self.text_render_events[0].get_font_color()

    def get_font_family(self):
        return self.text_render_events[0].get_font_family()

    def get_font_size(self):
        return self.text_render_events[0].get_font_size()

    def get_space_character_width_in_text_space(self):
        return self.text_render_events[0].get_space_character_width_in_text_space()

    def get_text(self):
        text = ""
        right = min(
            self.text_render_events[0].get_baseline().x0,
            self.text_render_events[0].get_baseline().x1,
        )
        for e in self.text_render_events:
            if e.get_text().startswith(" ") or text.endswith(" "):
                text += e.get_text()
                right = max(e.get_baseline().x0, e.get_baseline().x1)
                continue
            delta = abs(right - e.get_baseline().x0)
            space_width = round(e.get_space_character_width_in_text_space(), 1)
            right = max(e.get_baseline().x0, e.get_baseline().x1)
            text += " " if (space_width * Decimal(0.90) < delta) else ""
            text += e.get_text()
        return text

    def get_baseline(self):
        min_x = min(
            self.text_render_events[0].get_baseline().x0,
            self.text_render_events[0].get_baseline().x1,
        )
        max_x = min(
            self.text_render_events[0].get_baseline().x0,
            self.text_render_events[0].get_baseline().x1,
        )
        y = self.text_render_events[0].get_baseline().y0
        for e in self.text_render_events:
            min_x = min(min_x, e.get_baseline().x0, e.get_baseline().x1)
            max_x = max(max_x, e.get_baseline().x0, e.get_baseline().x1)
        return LineSegment(x0=min_x, y0=y, x1=max_x, y1=y)

    def get_bounding_box(self) -> Rectangle:
        ls = self.get_baseline()
        max_ascent = max(
            [
                x.get_font_ascent() * Decimal(0.001) * x.get_font_size()
                for x in self.text_render_events
            ]
        )
        return Rectangle(ls.x0, ls.y0, abs(ls.x1 - ls.x0), max_ascent)
