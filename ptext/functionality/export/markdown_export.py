from ptext.functionality.structure.list.bullet_list_render_event import (
    BulletListRenderEvent,
)
from ptext.functionality.structure.list.ordered_list_render_event import (
    OrderedListRenderEvent,
)
from ptext.functionality.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)
from ptext.functionality.structure.title.title_render_event import TitleRenderEvent
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.page.page import Page


class MarkdownExport(EventListener):
    def __init__(self):
        self.current_page = -1
        self.markdown_per_page = {}

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        elif isinstance(event, TitleRenderEvent):
            self._render_title(event)
        elif isinstance(event, BulletListRenderEvent):
            self._render_bullet_list(event)
        elif isinstance(event, OrderedListRenderEvent):
            self._render_ordered_list(event)
        elif isinstance(event, ParagraphRenderEvent):
            self._render_paragraph(event)

    def _begin_page(self, page: Page):
        self.current_page += 1
        self.markdown_per_page[self.current_page] = ""

    def _render_title(self, event: TitleRenderEvent):
        if not self.markdown_per_page[self.current_page].endswith("\n"):
            self.markdown_per_page[self.current_page] += "\n"
        self.markdown_per_page[self.current_page] += "".join(
            ["#" for i in range(0, event.level)]
        )
        self.markdown_per_page[self.current_page] += " "
        self.markdown_per_page[self.current_page] += event.get_text()
        if not event.get_text().endswith("\n"):
            self.markdown_per_page[self.current_page] += event.get_text()

    def _render_paragraph(self, event: ParagraphRenderEvent):
        if not self.markdown_per_page[self.current_page].endswith("\n"):
            self.markdown_per_page[self.current_page] += "\n"
        for evt in event.contained_events:
            if evt.get_text().endswith("\n"):
                self.markdown_per_page[self.current_page] += (
                    evt.get_text()[:-1] + "  \n"
                )
            else:
                self.markdown_per_page[self.current_page] += evt.get_text() + "  \n"
        self.markdown_per_page[self.current_page] += "\n"

    def _render_bullet_list(self, event: BulletListRenderEvent):
        if not self.markdown_per_page[self.current_page].endswith("\n"):
            self.markdown_per_page[self.current_page] += "\n"
        for evt in event.contained_events:
            if evt.get_text().endswith("\n"):
                self.markdown_per_page[self.current_page] += (
                    "+ " + evt.get_text()[1:-1] + "  \n"
                )
            else:
                self.markdown_per_page[self.current_page] += (
                    "+ " + evt.get_text() + "  \n"
                )

    def _render_ordered_list(self, event: OrderedListRenderEvent):
        if not self.markdown_per_page[self.current_page].endswith("\n"):
            self.markdown_per_page[self.current_page] += "\n"
        txts = []
        for e in event.contained_events:
            t = e.get_text()
            while t[0] in "0123456789.":
                t = t[1:]
            txts.append(t)
        while all([x.startswith(txts[0][0]) for x in txts]) and txts[0][0] in ")]-:; ":
            txts = [x[1:] for x in txts]
        for i, t in enumerate(txts):
            if t.endswith("\n"):
                self.markdown_per_page[self.current_page] += (
                    str(i + 1) + ". " + t[1:-1] + "  \n"
                )
            else:
                self.markdown_per_page[self.current_page] += (
                    str(i + 1) + ". " + t + "  \n"
                )
        self.markdown_per_page[self.current_page] += "\n"

    def get_markdown_per_page(self, page_number: int) -> str:
        return (
            self.markdown_per_page[page_number]
            if page_number in self.markdown_per_page
            else ""
        )
