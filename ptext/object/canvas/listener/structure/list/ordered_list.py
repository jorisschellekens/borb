from typing import List

from ptext.object.canvas.listener.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)


class OrderedListRenderEvent(ParagraphRenderEvent):
    def __init__(self, paragraph_render_events: List[ParagraphRenderEvent]):
        self.paragraph_render_events = paragraph_render_events

    def get_font_color(self):
        return self.paragraph_render_events[0].get_font_color()

    def get_font_family(self):
        return self.paragraph_render_events[0].get_font_family()

    def get_font_size(self):
        return self.paragraph_render_events[0].get_font_size()

    def get_space_character_width_in_text_space(self):
        return self.paragraph_render_events[0].get_space_character_width_in_text_space()

    def get_text(self):
        return "".join([x.get_text() for x in self.paragraph_render_events])
