from typing import List

from ptext.toolkit.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)


class OrderedListRenderEvent(ParagraphRenderEvent):
    def __init__(self, paragraph_render_events: List[ParagraphRenderEvent]):
        super(OrderedListRenderEvent, self).__init__(paragraph_render_events)  # type: ignore [arg-type]

    def get_text(self) -> str:
        return "".join([x.get_text() for x in self.contained_events])
