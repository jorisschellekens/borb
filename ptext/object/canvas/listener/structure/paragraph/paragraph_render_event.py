from typing import List

from ptext.object.canvas.geometry.line_segment import LineSegment
from ptext.object.canvas.geometry.rectangle import Rectangle
from ptext.object.canvas.listener.structure.line.line_render_event import (
    LineRenderEvent,
)


class ParagraphRenderEvent(LineRenderEvent):
    def __init__(self, line_render_events: List[LineRenderEvent]):
        self.line_render_events = line_render_events

    def get_font_color(self):
        return self.line_render_events[0].get_font_color()

    def get_font_family(self):
        return self.line_render_events[0].get_font_family()

    def get_font_size(self):
        return self.line_render_events[0].get_font_size()

    def get_space_character_width_in_text_space(self):
        return self.line_render_events[0].get_space_character_width_in_text_space()

    def get_text(self):
        return "".join([x.get_text() + "\n" for x in self.line_render_events])

    def get_baseline(self):
        min_x = min(
            self.line_render_events[0].get_baseline().x0,
            self.line_render_events[0].get_baseline().x1,
        )
        max_x = min(
            self.line_render_events[0].get_baseline().x0,
            self.line_render_events[0].get_baseline().x1,
        )
        y = self.line_render_events[0].get_baseline().y0
        for e in self.line_render_events:
            min_x = min(min_x, e.get_baseline().x0, e.get_baseline().x1)
            max_x = max(max_x, e.get_baseline().x0, e.get_baseline().x1)
        return LineSegment(x0=min_x, y0=y, x1=max_x, y1=y)

    def get_bounding_box(self) -> Rectangle:
        top = (
            self.line_render_events[0].get_bounding_box().y
            + self.line_render_events[0].get_bounding_box().height
        )
        btm = self.line_render_events[-1].get_bounding_box().y
        left = min([x.get_bounding_box().x for x in self.line_render_events])
        right = max(
            [
                x.get_bounding_box().x + x.get_bounding_box().width
                for x in self.line_render_events
            ]
        )
        return Rectangle(left, btm, (right - left), (top - btm))
