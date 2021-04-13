#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener exports a Page as an mp3 file, essentially reading the text on the Page
"""
import typing
from decimal import Decimal

from gtts import gTTS  # type: ignore [import]

from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import Paragraph
from ptext.pdf.page.page import Page
from ptext.toolkit.structure.simple_paragraph_extraction import (
    SimpleParagraphExtraction,
)


class PDFToMP3(SimpleParagraphExtraction):
    """
    This implementation of EventListener exports a Page as an mp3 file, essentially reading the text on the Page
    """

    def __init__(
        self,
        include_position: bool = True,
        language: str = "en",
        slow: bool = False,
    ):
        """
        Constructs a new PDFToMP3
        """
        super(PDFToMP3, self).__init__()

        # tts info
        self.include_position = include_position
        self.language = language
        self.slow = slow

        # page info
        self.text_to_speak_for_page: typing.Dict[int, str] = {}

    def _end_page(self, page: Page):
        super(PDFToMP3, self)._end_page(page)
        self.text_to_speak_for_page[self.current_page_number] = "".join(
            [
                self._get_text_for_paragraph(p, i, self.current_page_number)
                for i, p in enumerate(
                    self.paragraphs_per_page[self.current_page_number]
                )
            ]
        )

    def _get_text_for_x(self, bounding_box: Rectangle) -> str:
        assert self.current_page
        w = self.current_page.get_page_info().get_width()
        assert w is not None
        xs: typing.List[Decimal] = [Decimal(0), w * Decimal(0.33), w * Decimal(0.66), w]
        x = bounding_box.x + bounding_box.width * Decimal(0.5)
        if xs[0] <= x <= xs[1]:
            return "left"
        if xs[1] <= x <= xs[2]:
            return "center"
        if xs[2] <= x <= xs[3]:
            return "right"
        return ""

    def _get_text_for_y(self, bounding_box: Rectangle) -> str:
        assert self.current_page
        h = self.current_page.get_page_info().get_height()
        assert h is not None
        assert h is not None
        ys: typing.List[Decimal] = [h, h * Decimal(0.66), h * Decimal(0.33), Decimal(0)]
        y = bounding_box.y
        if ys[1] <= y <= ys[0]:
            return "top"
        if ys[2] <= y <= ys[1]:
            return "middle"
        if ys[3] <= y <= ys[2]:
            return "bottom"
        return ""

    def _get_text_for_paragraph(
        self, paragraph: Paragraph, paragraph_number: int, page_number: int
    ):

        # text to speak
        text_to_speak_for_paragraph = ""

        # position
        if self.include_position:
            assert paragraph.bounding_box is not None
            text_to_speak_for_paragraph += "Page %d, paragraph %d, %s %s." % (
                page_number + 1,
                paragraph_number + 1,
                self._get_text_for_y(paragraph.bounding_box),
                self._get_text_for_x(paragraph.bounding_box),
            )
        # text of paragraph
        text_to_speak_for_paragraph += paragraph.text

        # force period if needed
        if text_to_speak_for_paragraph[-1] not in ["?", "!", "."]:
            text_to_speak_for_paragraph += ". "

        # return
        return text_to_speak_for_paragraph

    def get_audio_file_per_page(self, page_number: int, path: str):
        """
        This function creates and then returns the audio-file for the text spoken at the given page
        """
        sound = gTTS(text=self.text_to_speak_for_page[page_number], lang=self.language)
        sound.save(path)
        return path
