from ptext.object.canvas.event.begin_page_event import BeginPageEvent
from ptext.object.canvas.event.end_page_event import EndPageEvent
from ptext.object.canvas.event.text_render_event import (
    TextRenderEvent,
)
from ptext.object.canvas.listener.structure.line.simple_line_render_event_factory import (
    SimpleLineRenderEventFactory,
)
from ptext.object.canvas.listener.structure.list.simple_bullet_list_factory import (
    SimpleBulletListFactory,
)
from ptext.object.canvas.listener.structure.list.simple_ordered_list_factory import (
    SimpleOrderedListFactory,
)
from ptext.object.canvas.listener.structure.paragraph.simple_paragraph_factory import (
    SimpleParagraphFactory,
)
from ptext.object.page.page import Page
from ptext.object.event_listener import Event, EventListener


class SimpleStructureExtraction(EventListener):
    def __init__(self):
        self.text_render_info_per_page = {}
        self.current_page = -1

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, TextRenderEvent):
            self.render_text(event)
        if isinstance(event, BeginPageEvent):
            self.begin_page(event.get_page())
        if isinstance(event, EndPageEvent):
            self.end_page(event.get_page())

    def render_text(self, text_render_info: TextRenderEvent):

        # init if needed
        if self.current_page not in self.text_render_info_per_page:
            self.text_render_info_per_page[self.current_page] = []

        # append TextRenderInfo
        self.text_render_info_per_page[self.current_page].append(text_render_info)

    def begin_page(self, page: Page):
        self.current_page += 1

    def end_page(self, page: Page):

        # get TextRenderInfo objects on page
        events = (
            self.text_render_info_per_page[self.current_page]
            if self.current_page in self.text_render_info_per_page
            else []
        )

        # remove no-op
        events = [x for x in events if len(x.get_text().replace(" ", "")) != 0]

        # skip empty
        if len(events) == 0:
            return

        # chunks to lines
        events = SimpleLineRenderEventFactory().create(events)
        for evt in events:
            page.event_occurred(evt)

        # lines to paragraphs
        events = SimpleParagraphFactory().create(events)
        for evt in events:
            page.event_occurred(evt)

        # paragraphs to lists
        for e in SimpleOrderedListFactory().create(events):
            page.event_occurred(e)
        for e in SimpleBulletListFactory().create(events):
            page.event_occurred(e)

        # TODO : extract tables
