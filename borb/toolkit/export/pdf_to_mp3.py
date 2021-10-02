#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener exports a Page as an mp3 file, essentially reading the text on the Page
"""
import tempfile
import typing
from decimal import Decimal
from pathlib import Path

from gtts import gTTS  # type: ignore [import]

from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_paragraph_extraction import SimpleParagraphExtraction


class PDFToMP3(SimpleParagraphExtraction):
    """
    This implementation of EventListener exports a Page as an mp3 file, essentially reading the text on the Page
    """

    @staticmethod
    def convert_pdf_to_mp3(file: Path, page_number: int) -> Path:
        """
        This function converts a PDF to an MP3 file, returning its Path
        """
        l: "PDFToMP3" = PDFToMP3()
        with open(file, "rb") as pdf_file_handle:
            PDF.loads(pdf_file_handle, [l])  # type: ignore [arg-type]
        temporary_file: Path = Path(
            tempfile.NamedTemporaryFile(prefix="pdf_to_mp3", suffix=".mp3").name
        )
        l.get_audio_for_page(page_number, str(temporary_file))
        return temporary_file

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
        self._include_position = include_position
        self._language = language
        self._speak_slowly = slow

        # page info
        self._text_to_speak_for_page: typing.Dict[int, str] = {}

    def _end_page(self, page: Page):
        super(PDFToMP3, self)._end_page(page)
        self._text_to_speak_for_page[self._current_page_number] = "".join(
            [
                self._get_text_for_paragraph(p, i, self._current_page_number)
                for i, p in enumerate(
                    self._paragraphs_per_page[self._current_page_number]
                )
            ]
        )

    def _get_text_for_x(self, bounding_box: Rectangle) -> str:
        assert self._current_page
        w = self._current_page.get_page_info().get_width()
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
        assert self._current_page
        h = self._current_page.get_page_info().get_height()
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
        if self._include_position:
            assert paragraph.bounding_box is not None
            text_to_speak_for_paragraph += "Page %d, paragraph %d, %s %s." % (
                page_number + 1,
                paragraph_number + 1,
                self._get_text_for_y(paragraph.bounding_box),
                self._get_text_for_x(paragraph.bounding_box),
            )
        # text of paragraph
        text_to_speak_for_paragraph += paragraph._text

        # force period if needed
        if text_to_speak_for_paragraph[-1] not in ["?", "!", "."]:
            text_to_speak_for_paragraph += ". "

        # return
        return text_to_speak_for_paragraph

    def get_audio_for_page(self, page_number: int, path: str):
        """
        This function creates and then returns the audio-file for the text spoken at the given page
        """
        sound = gTTS(
            text=self._text_to_speak_for_page[page_number], lang=self._language
        )
        sound.save(path)
        return path
