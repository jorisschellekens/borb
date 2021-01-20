from ptext.pdf.canvas.canvas_graphics_state import CanvasGraphicsState
from ptext.pdf.canvas.event.event_listener import Event
from ptext.pdf.canvas.geometry.line_segment import LineSegment


class LineRenderEvent(Event):
    """
    This implementation of Event is triggered right after the Canvas has processed a stroke-path instruction.
    """

    def __init__(self, graphics_state: CanvasGraphicsState, line_segment: LineSegment):
        super(LineRenderEvent, self).__init__()
        self.graphics_state = graphics_state
        self.line_segment = line_segment

    def get_line_segment(self) -> LineSegment:
        return self.line_segment
