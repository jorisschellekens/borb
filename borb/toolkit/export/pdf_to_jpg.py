#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener renders a PDF to a PIL Image
"""
import platform
import typing
from decimal import Decimal
from pathlib import Path

from PIL import Image as PILImage  # type: ignore [import]
from PIL import ImageDraw, ImageFont

from borb.pdf.canvas.color.color import Color
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from borb.toolkit.export.pdf_to_svg import PDFToSVG


class PDFToJPG(PDFToSVG):
    """
    This implementation of EventListener renders a PDF to a PIL Image
    """

    @staticmethod
    def convert_pdf_to_jpg(file: Path, page_number: int) -> PILImage:
        """
        This function converts a PDF to an PIL.Image
        """
        l: "PDFToJPG" = PDFToJPG()
        with open(file, "rb") as pdf_file_handle:
            PDF.loads(pdf_file_handle, [l])  # type: ignore [arg-type]
        return l.get_image_for_page(page_number)

    def __init__(
        self,
        default_page_width: Decimal = Decimal(PageSize.A4_PORTRAIT.value[0]),
        default_page_height: Decimal = Decimal(PageSize.A4_PORTRAIT.value[1]),
    ):
        super(PDFToJPG, self).__init__(
            default_page_width=default_page_width,
            default_page_height=default_page_height,
        )
        self._jpg_image_per_page: typing.Dict[int, PILImage] = {}

        # figure out fonts
        self._regular_font: typing.Optional[Path] = None
        self._bold_font: typing.Optional[Path] = None
        self._italic_font: typing.Optional[Path] = None
        self._bold_italic_font: typing.Optional[Path] = None
        self._find_font_families()

    def _find_font_families(self):
        system: str = platform.system()
        assert system in ["Darwin", "Linux", "Windows"]
        root_font_dir: typing.Optional[Path] = None
        if system == "Linux":
            root_font_dir = Path("/usr/share/fonts")
        if system == "Darwin":
            root_font_dir = Path("/Library/Fonts/")
        if system == "Windows":
            root_font_dir = Path("C:/Windows/Fonts")

        # BFS directory
        ttf_font_files = []
        file_stk: typing.List[Path] = [root_font_dir]
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
        for c in ["LiberationSans", "LiberationMono"]:
            suffixes = ["-Regular", "-Italic", "-Bold", "-BoldItalic"]
            all_fonts_present = all(
                [
                    y in [x.name for x in ttf_font_files]
                    for y in [c + x + ".ttf" for x in suffixes]
                ]
            )
            if all_fonts_present:
                self._regular_font = [
                    x for x in ttf_font_files if x.name.endswith(c + "-Regular.ttf")
                ][0]
                self._bold_font = [
                    x for x in ttf_font_files if x.name.endswith(c + "-Bold.ttf")
                ][0]
                self._italic_font = [
                    x for x in ttf_font_files if x.name.endswith(c + "-Italic.ttf")
                ][0]
                self._bold_italic_font = [
                    x for x in ttf_font_files if x.name.endswith(c + "-BoldItalic.ttf")
                ][0]

    def _begin_page(
        self, page_nr: Decimal, page_width: Decimal, page_height: Decimal
    ) -> None:
        self._jpg_image_per_page[int(page_nr)] = PILImage.new(
            "RGB", (page_width, page_height), color=(255, 255, 255)
        )

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
            (x, page_height - y),
            text,
            font=font,
            fill=(
                int(font_color.to_rgb().red),
                int(font_color.to_rgb().green),
                int(font_color.to_rgb().blue),
            ),
        )

    def _render_image(
        self,
        page_nr: Decimal,
        page_width: Decimal,
        page_height: Decimal,
        x: Decimal,
        y: Decimal,
        image_width: Decimal,
        image_height: Decimal,
        image: PILImage,
    ):
        page_image = self._jpg_image_per_page.get(int(page_nr))
        assert page_image is not None

        # resize
        image = image.resize((int(image_width), int(image_height)))

        # paste
        page_image.paste(image, (int(x), int(page_height - y - image_height)))

    def get_image_for_page(self, page_nr: int) -> PILImage:
        """
        This function returns the PIL.Image for a given page_nr
        """
        assert page_nr in self._jpg_image_per_page
        return self._jpg_image_per_page[page_nr]
