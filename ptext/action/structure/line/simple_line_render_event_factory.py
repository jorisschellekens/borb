from functools import cmp_to_key
from typing import List, Tuple

from ptext.action.structure.line.line_render_event import (
    LineRenderEvent,
)
from ptext.pdf.canvas.event.text_render_event import (
    TextRenderEvent,
    LeftToRightComparator,
)


class SimpleLineRenderEventFactory:
    def __init__(self):
        self.max_horizontal_gap = 20

    def create(
        self, text_render_events: List[TextRenderEvent]
    ) -> Tuple[List[TextRenderEvent], List[LineRenderEvent]]:

        # sort
        sorted(text_render_events, key=cmp_to_key(LeftToRightComparator.cmp))

        # build lines
        last_baseline = text_render_events[0]
        last_right = min(
            text_render_events[0].get_baseline().x0,
            text_render_events[0].get_baseline().x1,
        )
        text_render_event_buffer = []
        line_render_events = []
        for e in text_render_events:

            # check baseline
            y = e.get_baseline().y0
            if y != last_baseline:
                line_render_events.append(
                    self._build_line_from_events(text_render_event_buffer)
                )
                text_render_event_buffer = [e]
                last_baseline = y
                last_right = max(e.get_baseline().x0, e.get_baseline().x1)
                continue

            # check gap between previous chunk
            gap = last_right - min(e.get_baseline().x0, e.get_baseline().x1)
            if gap < self.max_horizontal_gap:
                text_render_event_buffer.append(e)
            else:
                line_render_events.append(
                    self._build_line_from_events(text_render_event_buffer)
                )
                text_render_event_buffer = [e]
            last_right = max(e.get_baseline().x0, e.get_baseline().x1)

        # last events in buffer
        line_render_events.append(
            self._build_line_from_events(text_render_event_buffer)
        )

        # return
        return [], [x for x in line_render_events if x != None]

    def _build_line_from_events(
        self, events_for_line: List[TextRenderEvent]
    ) -> LineRenderEvent:
        return (
            LineRenderEvent(text_render_events=events_for_line)
            if len(events_for_line) > 0
            else None
        )
