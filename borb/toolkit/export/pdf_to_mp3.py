#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of EventListener exports a Page as an mp3 file, essentially reading the text on the Page
"""
import io
import tempfile
import typing
from decimal import Decimal
import pathlib

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.toolkit.text.simple_paragraph_extraction import SimpleParagraphExtraction


class PDFToMP3(SimpleParagraphExtraction):
    """
    This implementation of EventListener exports a Page as an mp3 file (returned as bytes), essentially reading the text on the Page
    """

    #
    # CONSTRUCTOR
    #

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

    #
    # PRIVATE
    #

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

    def _get_text_for_paragraph(
        self, paragraph: Paragraph, paragraph_number: int, page_number: int
    ):
        # text to speak
        text_to_speak_for_paragraph = ""

        # position
        if self._include_position:
            lbox: typing.Optional[Rectangle] = paragraph.get_previous_layout_box()
            assert lbox is not None
            text_to_speak_for_paragraph += "Page %d, paragraph %d, %s %s." % (
                page_number + 1,
                paragraph_number + 1,
                self._get_text_for_y(lbox),
                self._get_text_for_x(lbox),
            )
        # text of paragraph
        text_to_speak_for_paragraph += paragraph.get_text()

        # force period if needed
        if text_to_speak_for_paragraph[-1] not in ["?", "!", "."]:
            text_to_speak_for_paragraph += ". "

        # return
        return text_to_speak_for_paragraph

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

    #
    # PUBLIC
    #

    @staticmethod
    def convert_pdf_to_mp3(pdf: Document) -> typing.Dict[int, bytes]:
        """
        This function converts a PDF to an MP3 file, returning its Path
        """
        sound_bytes_of_each_page: typing.Dict[int, bytes] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])

            # register EventListener
            cse: "PDFToMP3" = PDFToMP3()

            # process Page
            cse._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [cse])
            cse._event_occurred(EndPageEvent(page))

            # set in page
            sound_bytes_of_each_page[page_nr] = cse.convert_to_mp3()[0]

        # return
        return sound_bytes_of_each_page

    def convert_to_mp3(self) -> typing.Dict[int, bytes]:
        """
        This function creates and then returns the audio-file for the text spoken at the given page
        """
        import gtts  # type: ignore[import]

        sound_bytes_per_page: typing.Dict[int, bytes] = {}
        number_of_pages: int = len(self._text_to_speak_for_page.keys())
        for page_nr in range(0, number_of_pages):
            sound_for_page = gtts.gTTS(
                text=self._text_to_speak_for_page[page_nr], lang=self._language
            )

            # store in temporary location
            tmp_path: pathlib.Path = pathlib.Path(tempfile.NamedTemporaryFile().name)
            sound_for_page.save(tmp_path)

            # read bytes
            sound_bytes: typing.Optional[bytes] = None
            with open(tmp_path, "rb") as tmp_file_handle:
                sound_bytes = tmp_file_handle.read()
            assert sound_bytes is not None
            try:
                if tmp_path.exists():
                    tmp_path.unlink()
            except:
                pass
            # insert into dict
            sound_bytes_per_page[page_nr] = sound_bytes

        # return
        return sound_bytes_per_page
