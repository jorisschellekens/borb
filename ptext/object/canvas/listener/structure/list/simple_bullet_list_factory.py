from typing import List

from ptext.object.canvas.listener.structure.list.bullet_list import (
    BulletListRenderEvent,
)
from ptext.object.canvas.listener.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)


class SimpleBulletListFactory:
    def create(
        self, paragraph_render_events: List[ParagraphRenderEvent]
    ) -> List[ParagraphRenderEvent]:
        out_events = []
        i = 0
        while i < len(paragraph_render_events):
            if self._starts_with_bullet(paragraph_render_events[i].get_text()):

                # find consecutive list elements
                j = i + 1
                while (
                    self._starts_with_bullet(paragraph_render_events[j].get_text())
                    and abs(
                        paragraph_render_events[j].get_bounding_box().x
                        - paragraph_render_events[i].get_bounding_box().x
                    )
                    < 20
                    and j < len(paragraph_render_events)
                ):
                    j += 1

                # add list
                if abs(j - i) > 1:
                    out_events.append(
                        BulletListRenderEvent(paragraph_render_events[i:j])
                    )
                else:
                    out_events.append(paragraph_render_events[i])

                # skip
                i = j

            # next
            out_events.append(paragraph_render_events[i])
            i += 1

        # return
        return out_events

    def _starts_with_bullet(self, text: str):
        return text[0] in "0123456789"
