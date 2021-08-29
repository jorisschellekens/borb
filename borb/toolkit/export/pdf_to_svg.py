#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener renders a PDF to an SVG image
"""
import base64
import io
import typing
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.event_listener import Event, EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.page.page import Page
from borb.pdf.page.page_size import PageSize
from borb.pdf.pdf import PDF
from PIL import Image as PILImage  # type: ignore [import]


class PDFToSVG(EventListener):
    """
    This implementation of EventListener renders a PDF to an SVG image
    """

    @staticmethod
    def convert_pdf_to_svg(file: Path, page_number: int) -> ET.Element:
        """
        This function converts a PDF to an SVG ET.Element
        """
        l: "PDFToSVG" = PDFToSVG()
        with open(file, "rb") as pdf_file_handle:
            PDF.loads(pdf_file_handle, [l])  # type: ignore [arg-type]
        return l.get_image_for_page(page_number)

    def __init__(
        self,
        default_page_width: Decimal = Decimal(PageSize.A4_PORTRAIT.value[0]),
        default_page_height: Decimal = Decimal(PageSize.A4_PORTRAIT.value[1]),
    ):
        self._default_page_width = default_page_width
        self._default_page_height = default_page_height
        self._page: typing.Optional[Page] = None
        self._page_nr = Decimal(-1)
        self._svg_per_page: typing.Dict[int, ET.Element] = {}

    def _event_occurred(self, event: Event) -> None:
        # BeginPageEvent
        if isinstance(event, BeginPageEvent):
            self._page_nr += Decimal(1)
            self._page = event.get_page()
            self._begin_page(
                self._page_nr,
                self._page.get_page_info().get_width() or self._default_page_width,
                self._page.get_page_info().get_height() or self._default_page_height,
            )
        # ImageRenderEvent
        if isinstance(event, ImageRenderEvent):
            assert self._page is not None
            self._render_image(
                self._page_nr,
                self._page.get_page_info().get_width() or self._default_page_width,
                self._page.get_page_info().get_height() or self._default_page_height,
                event.get_x(),
                event.get_y(),
                event.get_width(),
                event.get_height(),
                event.get_image(),
            )
        # ChunkOfTextRenderEvent
        if isinstance(event, ChunkOfTextRenderEvent):
            assert self._page is not None
            font_name_as_str = "Helvetica"
            if event._font.get_font_name():
                font_name_as_str = str(event._font.get_font_name())
            self._render_text(
                self._page_nr,
                self._page.get_page_info().get_width() or self._default_page_width,
                self._page.get_page_info().get_height() or self._default_page_height,
                event.get_baseline().get_x(),
                event.get_baseline().get_y(),
                event._font_color,
                event._font_size,
                font_name_as_str.replace("#20", " ")
                .replace(",Bold", "")
                .replace(",bold", "")
                .replace("Bold", "")
                .replace("bold", "")
                .replace(",Italic", "")
                .replace(",italic", "")
                .replace("Italic", "")
                .replace("italic", ""),
                "BOLD" in font_name_as_str.upper(),
                "ITALIC" in font_name_as_str.upper(),
                event._text,
            )

    def _begin_page(
        self, page_nr: Decimal, page_width: Decimal, page_height: Decimal
    ) -> None:

        # init svg image
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        svg_element = ET.Element("svg")
        svg_element.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        svg_element.set("viewbox", "0 0 %d %d" % (page_width, page_height))

        # white background
        rct_element = ET.Element("rect")
        rct_element.set("width", str(page_width))
        rct_element.set("height", str(page_height))
        rct_element.set("style", "fill:rgb(255, 255, 255);")
        svg_element.append(rct_element)
        self._svg_per_page[int(page_nr)] = svg_element  # type: ignore [assignment]

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

        text_element = ET.Element("text")

        # bold
        if bold:
            text_element.set("_font-weight", "bold")

        # italic
        if italic:
            text_element.set("_font-style", "italic")

        # font_color, font_size, preserve space
        font_color_rgb = font_color.to_rgb()
        text_element.set(
            "style",
            "fill:rgb(%d, %d, %d); _font-size:%d px; white-space: pre;"
            % (
                font_color_rgb.red,
                font_color_rgb.green,
                font_color_rgb.blue,
                int(font_size),
            ),
        )
        text_element.set("xml:space", "preserve")

        # set font-family
        text_element.set("_font-family", font_name)

        # text
        text_element.text = text

        # position
        text_element.set("x", str(int(x)))
        text_element.set("y", str(int(page_height - y)))

        # append
        assert self._svg_per_page[int(page_nr)] is not None
        self._svg_per_page[int(page_nr)].append(text_element)

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
        pass

        # base64 image
        with io.BytesIO() as output:
            image.convert("RGB").save(output, format="JPEG")
            base64_image = "data:image/png;base64," + base64.b64encode(
                output.getvalue()
            ).decode("utf-8")

        image_element = ET.Element("image")
        image_element.set("width", str(int(image_width)))
        image_element.set("height", str(int(image_height)))
        image_element.set("xlink:href", base64_image)

        # position
        image_element.set("x", str(int(x)))
        image_element.set("y", str(int(page_height - y - image_height)))

        # append
        assert self._svg_per_page[int(page_nr)] is not None
        self._svg_per_page[int(page_nr)].append(image_element)

    def get_image_for_page(self, page_nr: int) -> ET.Element:
        """
        This function returns the ET.Element for a given page_nr
        """
        assert page_nr in self._svg_per_page
        return self._svg_per_page[page_nr]
