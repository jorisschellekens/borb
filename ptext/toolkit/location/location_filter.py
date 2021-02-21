import typing

from ptext.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.geometry.rectangle import Rectangle


class LocationFilter(EventListener):
    def __init__(self, x0: float, y0: float, x1: float, y1: float):
        if x0 > x1:
            raise ValueError("x0 should be smaller than x1")
        if y0 > y1:
            raise ValueError("y0 should be smaller than y1")
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.listeners: typing.List[EventListener] = []

    def add_listener(self, listener: "EventListener") -> "LocationFilter":
        self.listeners.append(listener)
        return self

    def event_occurred(self, event: "Event") -> None:
        # filter TextRenderEvent
        if isinstance(event, ChunkOfTextRenderEvent):
            bb: typing.Optional[Rectangle] = event.get_bounding_box()
            assert bb is not None
            if self.x0 < bb.x < self.x1 and self.y0 < bb.y < self.y1:
                for l in self.listeners:
                    l.event_occurred(event)
            return

        # filter ImageRenderEvent
        if isinstance(event, ImageRenderEvent):
            if self.x0 < event.get_x() < self.x1 and self.y0 < event.get_y() < self.y1:
                for l in self.listeners:
                    l.event_occurred(event)
            return

        # default
        for l in self.listeners:
            l.event_occurred(event)
