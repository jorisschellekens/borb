from ptext.object.page.page import Page
from ptext.object.pdf_high_level_object import Event


class BeginPageEvent(Event):
    def __init__(self, page: Page):
        self.page = page

    def get_page(self) -> Page:
        return self.page
