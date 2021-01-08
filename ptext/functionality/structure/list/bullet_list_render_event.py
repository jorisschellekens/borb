from typing import List

from ptext.functionality.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)


class BulletListRenderEvent(ParagraphRenderEvent):
    def __init__(self, paragraph_render_events: List[ParagraphRenderEvent]):
        super(BulletListRenderEvent, self).__init__(paragraph_render_events)  # type: ignore [arg-type]

    def get_text(self) -> str:
        return "".join([x.get_text() for x in self.contained_events])
