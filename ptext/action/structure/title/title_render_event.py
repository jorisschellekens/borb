from typing import List, Optional

from ptext.action.structure.paragraph.paragraph_render_event import ParagraphRenderEvent


class TitleRenderEvent(ParagraphRenderEvent):
    def __init__(
        self,
        paragraph_render_events: List[ParagraphRenderEvent],
        level: Optional[int] = None,
    ):
        super(TitleRenderEvent, self).__init__(paragraph_render_events)  # type: ignore [arg-type]
        self.level = 1
        if level is not None:
            self.level = level

    def get_level(self) -> int:
        return self.level
