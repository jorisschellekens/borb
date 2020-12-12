from typing import List

from ptext.action.structure.paragraph import (
    ParagraphRenderEvent,
)


class OrderedListRenderEvent(ParagraphRenderEvent):
    def __init__(self, paragraph_render_events: List[ParagraphRenderEvent]):
        super(OrderedListRenderEvent, self).__init__(paragraph_render_events)

    def get_text(self):
        return "".join([x.get_text() for x in self.contained_events])
