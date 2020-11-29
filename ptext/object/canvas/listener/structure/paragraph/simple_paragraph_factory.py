from decimal import Decimal
from math import sqrt
from statistics import median
from typing import List, Optional

from ptext.object.canvas.geometry.line_segment import LineSegment
from ptext.object.canvas.listener.structure.line.line_render_event import (
    LineRenderEvent,
)
from ptext.object.canvas.listener.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)


class SimpleParagraphFactory:
    def __init__(self):
        self.min_text_line_overlap = 0.8

    def create(self, line_render_events: List[LineRenderEvent]) -> ParagraphRenderEvent:

        # calculate average gap
        gaps = []
        for i in range(0, len(line_render_events) - 1):
            b0 = line_render_events[i].get_baseline()
            b1 = line_render_events[i + 1].get_baseline()
            if (
                self._overlap(b0, b1) / min(b0.length(), b1.length())
                > self.min_text_line_overlap
            ):
                gaps.append(abs(b0.y0 - b1.y0))
        avg_gap = median(gaps)
        std_dev_gap = sqrt(sum([(x - avg_gap) ** 2 for x in gaps]) / len(gaps))

        paragraph_render_events = []
        line_render_event_buffer = []
        last_baseline = line_render_events[0].get_baseline()
        for e in line_render_events:
            overlap = self._overlap(last_baseline, e.get_baseline()) / min(
                last_baseline.length(), e.get_baseline().length()
            )

            # check overlap with previous line
            if overlap < self.min_text_line_overlap:
                paragraph_render_events.append(
                    self._build_paragraph_from_lines(line_render_event_buffer)
                )
                line_render_event_buffer = [e]
                last_baseline = e.get_baseline()

            # check gap
            gap = abs(last_baseline.y0 - e.get_baseline().y0)
            if gap < avg_gap * Decimal(1.25):
                line_render_event_buffer.append(e)
                last_baseline = e.get_baseline()
            else:
                paragraph_render_events.append(
                    self._build_paragraph_from_lines(line_render_event_buffer)
                )
                line_render_event_buffer = [e]
                last_baseline = e.get_baseline()

        paragraph_render_events.append(
            self._build_paragraph_from_lines(line_render_event_buffer)
        )

        # return
        return paragraph_render_events

    def _overlap(self, l0: LineSegment, l1: LineSegment) -> float:
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
