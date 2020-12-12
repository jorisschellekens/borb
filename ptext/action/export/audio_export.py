from decimal import Decimal

from gtts import gTTS

from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.action.structure.paragraph import (
    ParagraphRenderEvent,
)
from ptext.pdf.page.page import Page
from ptext.pdf.canvas.event.event_listener import EventListener, Event


class AudioExport(EventListener):
    """
    This implementation of EventListener exports a Page as an mp3 file, essentially reading the text on the Page
    """

    def __init__(self):

        # tts info
        self.include_position = True
        self.language = "en"
        self.slow = False

        # page info
        self.text_to_speak_for_page = {}
        self.current_paragraph = -1
        self.current_page = -1
        self.current_page_size = None

    def event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, ParagraphRenderEvent):
            self._speak_paragraph(event)

    def _begin_page(self, page: Page):
        self.current_page += 1
        self.current_page = 0
        self.current_page_size = page.get_page_info().get_size()

    def _speak_paragraph(self, event: ParagraphRenderEvent):
        self.current_paragraph += 1

        # text to speak
        text_to_speak_for_paragraph = ""

        # position
        if self.include_position:
            mid_x = (
                event.get_bounding_box().x
                + event.get_bounding_box().height / Decimal(2)
            )
            mid_y = (
                event.get_bounding_box().y + event.get_bounding_box().width / Decimal(2)
            )

            xs = [
                0,
                int(self.current_page_size[0] / 3),
                2 * int(self.current_page_size[0] / 3),
                int(self.current_page_size[0]),
            ]
            xs_names = ["left", "middle", "right"]

            ys = [
                0,
                int(self.current_page_size[1] / 3),
                2 * int(self.current_page_size[1] / 3),
                int(self.current_page_size[1]),
            ]
            ys_names = ["top", "middle", "bottom"]

            x_name = None
            y_name = None
            for i in range(0, len(xs) - 1):
                if xs[i] <= mid_x <= xs[i + 1]:
                    x_name = xs_names[i]
            for i in range(0, len(ys) - 1):
                if ys[i] <= mid_y <= ys[i + 1]:
                    y_name = ys_names[i]

            text_to_speak_for_paragraph += (
                "Page %d, paragraph %d, located at %s %s. "
                % (self.current_page + 1, self.current_paragraph, x_name, y_name)
            )

        text_to_speak_for_paragraph += event.get_text()

        # append to text_to_speak_for_page
        if self.current_page not in self.text_to_speak_for_page:
            self.text_to_speak_for_page[self.current_page] = ""
        self.text_to_speak_for_page[self.current_page] += text_to_speak_for_paragraph

    def get_audio_file_per_page(self, page_number: int, path: str):
        sound = gTTS(text=self.text_to_speak_for_page[page_number], lang=self.language)
        sound.save(path)
        return path
