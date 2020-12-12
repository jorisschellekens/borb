from typing import List, Tuple

from ptext.action.structure.list import (
    BulletListRenderEvent,
)
from ptext.action.structure.paragraph import (
    ParagraphRenderEvent,
)


class SimpleBulletListFactory:
    def create(
        self, paragraph_render_events: List[ParagraphRenderEvent]
    ) -> Tuple[List[ParagraphRenderEvent], List[BulletListRenderEvent]]:
        selected_events = []
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
                    selected_events.append(
                        BulletListRenderEvent(paragraph_render_events[i:j])
                    )

                # skip
                i = j

            i += 1

        # return
        to_remove = []
        for x in selected_events:
            to_remove.extend(x.contained_events)
        return [
            x for x in paragraph_render_events if x not in to_remove
        ], selected_events

    def _starts_with_bullet(self, text: str):
        return text[0] in "0123456789"
