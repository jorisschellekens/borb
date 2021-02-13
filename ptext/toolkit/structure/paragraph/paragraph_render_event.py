from typing import List

from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.toolkit.structure.line.line_render_event import (
    LineRenderEvent,
)


class ParagraphRenderEvent(LineRenderEvent):
    def __init__(self, line_render_events: List[LineRenderEvent]):
        super(ParagraphRenderEvent, self).__init__(line_render_events)  # type: ignore [arg-type]

    def get_text(self) -> str:
        return "".join([x.get_text() + "\n" for x in self.contained_events])

    def get_bounding_box(self) -> Rectangle:
        assert isinstance(self.contained_events[0], LineRenderEvent)
        assert isinstance(self.contained_events[-1], LineRenderEvent)
        top = (
            self.contained_events[0].get_bounding_box().y
            + self.contained_events[0].get_bounding_box().height
        )
        btm = self.contained_events[-1].get_bounding_box().y
        left = self.contained_events[0].get_bounding_box().x
        right = self.contained_events[0].get_bounding_box().x
        for e in self.contained_events:
            assert isinstance(e, LineRenderEvent)
            left = min(e.get_bounding_box().x, left)
            right = min(e.get_bounding_box().x + e.get_bounding_box().width, left)
        return Rectangle(left, btm, (right - left), (top - btm))
