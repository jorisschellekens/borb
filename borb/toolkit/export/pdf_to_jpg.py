#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener renders a PDF to a PIL Image
"""
import io
import platform
import typing
from decimal import Decimal
import pathlib

from PIL import Image as PILImageModule
from PIL import ImageDraw
from PIL import ImageFont

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.page.page import Page
from borb.pdf.page.page_size import PageSize
from borb.toolkit.export.pdf_to_svg import PDFToSVG


class PDFToJPG(PDFToSVG):
    """
    This implementation of EventListener renders a PDF to a PIL Image
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        default_page_width: Decimal = Decimal(PageSize.A4_PORTRAIT.value[0]),
        default_page_height: Decimal = Decimal(PageSize.A4_PORTRAIT.value[1]),
    ):
        super(PDFToJPG, self).__init__(
            default_page_width=default_page_width,
            default_page_height=default_page_height,
        )
        self._jpg_image_per_page: typing.Dict[int, PILImageModule.Image] = {}  # type: ignore[valid-type]

        # figure out fonts
        self._regular_font: typing.Optional[pathlib.Path] = None
        self._bold_font: typing.Optional[pathlib.Path] = None
        self._italic_font: typing.Optional[pathlib.Path] = None
        self._bold_italic_font: typing.Optional[pathlib.Path] = None
        self._find_font_families()

    #
    # PRIVATE
    #

    def _begin_page(
        self, page_nr: Decimal, page_width: Decimal, page_height: Decimal
    ) -> None:
        self._jpg_image_per_page[int(page_nr)] = PILImageModule.new(
            "RGB", (int(page_width), int(page_height)), color=(255, 255, 255)
        )

    def _find_font_families(self):
        system: str = platform.system()
        assert system in ["Darwin", "Linux", "Windows"]
        root_font_dir: typing.Optional[pathlib.Path] = None
        if system == "Linux":
            root_font_dir = pathlib.Path("/usr/share/fonts")
        if system == "Darwin":
            root_font_dir = pathlib.Path("/Library/Fonts/")
        if system == "Windows":
            root_font_dir = pathlib.Path("C:/Windows/Fonts")

        # BFS directory
        ttf_font_files = []
        file_stk: typing.List[pathlib.Path] = [root_font_dir]
        while len(file_stk) > 0:
            f = file_stk[0]
            file_stk.pop(0)
            if f.is_dir():
                for subdir in f.iterdir():
                    file_stk.append(subdir)
            else:
                if f.name.endswith(".ttf"):
                    ttf_font_files.append(f)

        # find family of fonts
        for c in ["LiberationSans", "LiberationMono", "arial"]:
            # fmt: off
            suffixes: typing.List[str] = ["-Regular", "-Italic", "-Bold", "-BoldItalic"]
            all_fonts_present = all([y in [x.name for x in ttf_font_files]for y in [c + x + ".ttf" for x in suffixes]])
            if all_fonts_present:
                self._regular_font = [x for x in ttf_font_files if x.name.endswith(c + "-Regular.ttf")][0]
                self._bold_font = [x for x in ttf_font_files if x.name.endswith(c + "-Bold.ttf")][0]
                self._italic_font = [x for x in ttf_font_files if x.name.endswith(c + "-Italic.ttf")][0]
                self._bold_italic_font = [x for x in ttf_font_files if x.name.endswith(c + "-BoldItalic.ttf")][0]
            # fmt: on

            # fmt: off
            suffixes = ["", "i", "bd", "bi"]
            all_fonts_present = all([y in [x.name for x in ttf_font_files]for y in [c + x + ".ttf" for x in suffixes]])
            if all_fonts_present:
                self._regular_font = [x for x in ttf_font_files if x.name.endswith(c + ".ttf")][0]
                self._bold_font = [x for x in ttf_font_files if x.name.endswith(c + "bd.ttf")][0]
                self._italic_font = [x for x in ttf_font_files if x.name.endswith(c + "i.ttf")][0]
                self._bold_italic_font = [x for x in ttf_font_files if x.name.endswith(c + "bi.ttf")][0]
            # fmt: on

    def _render_image(
        self,
        page_nr: Decimal,
        page_width: Decimal,
        page_height: Decimal,
        x: Decimal,
        y: Decimal,
        image_width: Decimal,
        image_height: Decimal,
        image: PILImageModule.Image,  # type: ignore[valid-type]
    ):
        page_image = self._jpg_image_per_page.get(int(page_nr))
        assert page_image is not None

        # resize
        image = image.resize((int(image_width), int(image_height)))

        # paste
        page_image.paste(image, (int(x), int(page_height - y - image_height)))

    def _render_text(
        self,
        page_nr: Decimal,
        page_width: Decimal,
        page_height: Decimal,
        x: Decimal,
        y: Decimal,
        font_color: Color,
        font_size: Decimal,
        font_name: str,
        bold: bool,
        italic: bool,
        text: str,
    ):
        if len(text.strip()) == 0:
            return

        assert self._bold_font
        assert self._bold_italic_font
        assert self._italic_font
        assert self._regular_font

        font_path = self._regular_font
        if bold and italic:
            font_path = self._bold_italic_font
        elif bold:
            font_path = self._bold_font
        elif italic:
            font_path = self._italic_font

        # instantiate font
        font = ImageFont.truetype(str(font_path), int(font_size))

        # draw text
        assert self._jpg_image_per_page.get(int(page_nr)) is not None
        draw = ImageDraw.Draw(self._jpg_image_per_page[int(page_nr)])
        draw.text(
            (float(x), float(page_height - y)),
            text,
            font=font,
            fill=(
                int(font_color.to_rgb().red),
                int(font_color.to_rgb().green),
                int(font_color.to_rgb().blue),
            ),
        )

    #
    # PUBLIC
    #

    @staticmethod
    def convert_pdf_to_jpg(pdf: "Document") -> typing.Dict[int, PILImageModule.Image]:  # type: ignore[name-defined]
        """
        This function converts a PDF to an PIL.Image.Image
        """
        image_of_each_page: typing.Dict[int, PILImageModule.Image] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])

            # register EventListener
            cse: "PDFToJPG" = PDFToJPG()

            # process Page
            cse._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [cse])
            cse._event_occurred(EndPageEvent(page))

            # set in page
            image_of_each_page[page_nr] = cse.convert_to_jpg()[0]

        # return
        return image_of_each_page

    def convert_to_jpg(self) -> typing.Dict[int, PILImageModule.Image]:  # type: ignore[valid-type]
        """
        This function returns the PIL.Image for a given page_nr
        """
        return self._jpg_image_per_page
