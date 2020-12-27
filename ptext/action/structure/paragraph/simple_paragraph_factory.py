from typing import List, Optional, Tuple

from ptext.action.structure.line.line_render_event import (
    LineRenderEvent,
)
from ptext.action.structure.paragraph.paragraph_render_event import ParagraphRenderEvent
from ptext.pdf.canvas.datastructure.disjoint_set import disjointset
from ptext.pdf.canvas.geometry.line_segment import LineSegment


class SimpleParagraphFactory:
    def __init__(self):
        self.min_text_line_overlap = 0.8
        self.max_multiplied_leading = 1.2

    def create(
        self, line_render_events: List[LineRenderEvent]
    ) -> Tuple[List[LineRenderEvent], List[ParagraphRenderEvent]]:

        ds = disjointset()
        for e in line_render_events:
            ds.add(e)

        for e0 in line_render_events:
            for e1 in line_render_events:
                if e0 is e1:
                    continue
                # get baselines
                b0 = e0.get_baseline()
                b1 = e1.get_baseline()

                # calculate leading
                leading = abs(b0.y0 - b1.y0) / max(
                    e0.get_font_size(), e0.get_font_size()
                )

                # vertical overlap
                overlap = self._overlap(b0, b1) / min(b0.length(), b1.length())

                # union
                if (
                    leading < self.max_multiplied_leading
                    and overlap > self.min_text_line_overlap
                ):
                    ds.union(e0, e1)
                else:
                    continue

        # return
        return [], [self._build_paragraph_from_lines(x) for x in ds.sets()]

    def _overlap(self, l0: LineSegment, l1: LineSegment) -> float:
        # lines do not overlap (l0 is left)
        if max(l0.x0, l0.x1) < min(l1.x0, l1.x1):
            return 0
        # lines do not overlap (l1 is left)
        if max(l1.x0, l1.x1) < min(l0.x0, l0.x1):
            return 0
        x0 = max(min(l0.x0, l0.x1), min(l1.x0, l1.x1))
        x1 = min(max(l0.x0, l0.x1), max(l1.x0, l1.x1))
        return abs(x1 - x0)

    def _build_paragraph_from_lines(
        self, line_render_events: List[LineRenderEvent]
    ) -> Optional[ParagraphRenderEvent]:
        return (
            ParagraphRenderEvent(line_render_events)
            if len(line_render_events) > 0
            else None
        )
