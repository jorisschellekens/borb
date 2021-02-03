import typing
from decimal import Decimal
from typing import Tuple

from gtts import gTTS  # type: ignore [import]

from ptext.functionality.structure.paragraph.paragraph_render_event import (
    ParagraphRenderEvent,
)
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.page.page import Page
from ptext.pdf.page.page_size import PageSize


class AudioExport(EventListener):
    """
    This implementation of EventListener exports a Page as an mp3 file, essentially reading the text on the Page
    """

    def __init__(
        self,
        include_position: bool = True,
        language: str = "en",
        slow: bool = False,
        default_page_size: Tuple[int, int] = PageSize.A4_PORTRAIT.value,
    ):
        """
        Constructs a new AudioExport
        """

        # tts info
        self.include_position = include_position
        self.language = language
        self.slow = slow

        # page info
        self.text_to_speak_for_page: typing.Dict[int, str] = {}
        self.current_paragraph = -1
        self.current_page: int = -1
        self.current_page_size: typing.Optional[Tuple[int, int]] = None
        self.default_page_size: Tuple[int, int] = default_page_size

    def event_occurred(self, event: "Event") -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, ParagraphRenderEvent):
            self._speak_paragraph(event)

    def _begin_page(self, page: "Page"):
        self.current_page += 1
        self.current_page = 0
        self.current_page_size = (
            page.get_page_info().get_size() or self.default_page_size
        )

    def _speak_paragraph(self, event: "ParagraphRenderEvent"):
        self.current_paragraph += 1

        # text to speak
        text_to_speak_for_paragraph = ""

        # position
        assert self.current_page_size is not None
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
