from ptext.object.canvas.event.text_render_event import TextRenderEvent
from ptext.object.event_listener import EventListener, Event


class SimpleTableExtraction(EventListener):
    def __init__(self):
        pass

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, TextRenderEvent):
            self.render_text(event)

    def render_text(self, event: TextRenderEvent) -> None:
        pass
