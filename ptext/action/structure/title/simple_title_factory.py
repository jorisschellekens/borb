from typing import List, Tuple

from ptext.action.structure.paragraph.paragraph_render_event import ParagraphRenderEvent
from ptext.action.structure.title.title_render_event import TitleRenderEvent


class SimpleTitleFactory:
    def create(
        self, paragraph_render_events: List[ParagraphRenderEvent]
    ) -> Tuple[List[ParagraphRenderEvent], List[TitleRenderEvent]]:

        # determine font size in which the majority of text is written
        font_size_count = {}
        for p in paragraph_render_events:
            font_size = p.get_font_size()
            number_of_characters = len(p.get_text())
            if font_size not in font_size_count:
                font_size_count[font_size] = 0
            font_size_count[font_size] += number_of_characters

        dominant_font_size = [
            k
            for k, v in font_size_count.items()
            if v == max([v for k, v in font_size_count.items()])
        ][0]

        # find all events that consist of 1 line, are completely in the same font,
        # and whose font size is bigger than the dominant font size
        selected_events = [
            TitleRenderEvent([x], level=1)
            for x in paragraph_render_events
            if len(x.contained_events) == 1
            and self._all_same_font(x)
            and x.get_font_size() > dominant_font_size
        ]

        # sort (larger font > bold)
        # TODO

        # assign levels
        level = 1
        for i in range(0, len(selected_events)):
            if i == 0:
                selected_events[i].level = level
                continue
            if self._is_different_level(selected_events[i - 1], selected_events[i]):
                level += 1
                selected_events[i].level = level
                continue
            selected_events[i].level = level

        # default
        to_remove = []
        for x in selected_events:
            to_remove.extend(x.contained_events)
        return [
            x for x in paragraph_render_events if x not in to_remove
        ], selected_events

    def _all_same_font(self, paragraph_render_event: ParagraphRenderEvent) -> bool:
        text_render_events = []
        for line_render_event in paragraph_render_event.contained_events:
            for text_render_event in line_render_event.contained_events:
                text_render_events.append(text_render_event)

        # determine family and size
        font_family = text_render_events[0].font_family
        font_size = text_render_events[0].font_size

        if any([x.font_family != font_family for x in text_render_events]):
            return False
        if any([x.font_size != font_size for x in text_render_events]):
            return False

        # default
        return True

    def _is_different_level(self, e0: ParagraphRenderEvent, e1: ParagraphRenderEvent):
        return (
            e0.get_font_family() != e1.get_font_family()
            or e0.get_font_size() != e1.get_font_size()
        )
