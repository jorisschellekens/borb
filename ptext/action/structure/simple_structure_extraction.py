from ptext.action.structure.line.simple_line_render_event_factory import (
    SimpleLineRenderEventFactory,
)
from ptext.action.structure.list.simple_bullet_list_factory import (
    SimpleBulletListFactory,
)
from ptext.action.structure.list.simple_ordered_list_factory import (
    SimpleOrderedListFactory,
)
from ptext.action.structure.paragraph.simple_paragraph_factory import (
    SimpleParagraphFactory,
)
from ptext.action.structure.title.simple_title_factory import SimpleTitleFactory
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.end_page_event import EndPageEvent
from ptext.pdf.canvas.event.event_listener import Event, EventListener
from ptext.pdf.canvas.event.text_render_event import (
    TextRenderEvent,
)
from ptext.pdf.page.page import Page


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
        text_render_events = (
            self.text_render_info_per_page[self.current_page]
            if self.current_page in self.text_render_info_per_page
            else []
        )

        # remove no-op
        text_render_events = [
            x for x in text_render_events if len(x.get_text().replace(" ", "")) != 0
        ]

        # skip empty
        if len(text_render_events) == 0:
            return

        # chunks to lines
        text_render_events, line_render_events = SimpleLineRenderEventFactory().create(
            text_render_events
        )

        # lines to paragraphs
        line_render_events, paragraph_render_events = SimpleParagraphFactory().create(
            line_render_events
        )

        # paragraphs to lists
        (
            paragraph_render_events,
            list_render_events_a,
        ) = SimpleOrderedListFactory().create(paragraph_render_events)
        (
            paragraph_render_events,
            list_render_events_b,
        ) = SimpleBulletListFactory().create(paragraph_render_events)

        # titles
        paragraph_render_events, title_events = SimpleTitleFactory().create(
            paragraph_render_events
        )

        # TODO : extract tables

        # fire events
        for e in (
            title_events
            + list_render_events_a
            + list_render_events_b
            + paragraph_render_events
            + line_render_events
        ):
            page.event_occurred(e)
