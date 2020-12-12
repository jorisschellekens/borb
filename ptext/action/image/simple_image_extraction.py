from typing import List

from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.page.page import Page
from ptext.pdf.canvas.event.event_listener import EventListener, Event


class SimpleImageExtraction(EventListener):
    def __init__(self):
        self.image_render_info_per_page = {}
        self.current_page = -1

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self.begin_page(event.get_page())
        if isinstance(event, ImageRenderEvent):
            self.render_image(event)

    def get_images_per_page(self, page_nr: int) -> List["PIL.Image.Image"]:
        return (
            self.image_render_info_per_page[page_nr]
            if page_nr in self.image_render_info_per_page
            else []
        )

    def render_image(self, image_render_event: ImageRenderEvent):

        # init if needed
        if self.current_page not in self.image_render_info_per_page:
            self.image_render_info_per_page[self.current_page] = []

        # append ImageRenderEvent
        self.image_render_info_per_page[self.current_page].append(
            image_render_event.get_image()
        )

    def begin_page(self, page: Page):
        self.current_page += 1
