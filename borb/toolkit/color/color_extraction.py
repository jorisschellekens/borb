#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener  extracts the colors used in rendering a PDF
"""
import io
import typing
from decimal import Decimal

from PIL import Image as PILImageModule

from borb.pdf.canvas.canvas import Canvas
from borb.pdf.canvas.canvas_stream_processor import CanvasStreamProcessor
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HSVColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page


class ColorExtraction(EventListener):
    """
    This implementation of EventListener  extracts the colors used in rendering a PDF
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        max_number_of_colors_to_return: int = 32,
        max_number_of_colors_to_register: int = 32,
    ):
        """
        Constructs a new ColorSpectrumExtraction
        """
        assert (
            max_number_of_colors_to_return >= 0
        ), "max_number_of_colors_to_return must be a positive integer"
        assert (
            max_number_of_colors_to_register >= 0
        ), "max_number_of_colors_to_register must be a positive integer"
        self._max_number_of_colors_to_return: int = max_number_of_colors_to_return
        self._max_number_of_colors_to_register: int = max_number_of_colors_to_register

        # build color_palette
        self._colors_from_palette_per_page: typing.Dict[
            int, typing.Dict[Color, Decimal]
        ] = {}
        self._color_palette: typing.List[Color] = [
            HSVColor(Decimal(x / 360), Decimal(1), Decimal(1)).to_rgb()
            for x in range(0, 360, self._max_number_of_colors_to_register)
        ]

        # keep track of current_page
        self._current_page: int = -1

    #
    # PRIVATE
    #

    def _begin_page(self, page: Page):
        self._current_page += 1
        self._colors_from_palette_per_page[self._current_page] = {}

    @staticmethod
    def _color_distance(c0: Color, c1: Color) -> Decimal:
        rgb0: RGBColor = c0.to_rgb()
        rgb1: RGBColor = c1.to_rgb()
        return (
            (rgb0.red - rgb1.red) ** 2
            + (rgb0.green - rgb1.green) ** 2
            + (rgb0.blue - rgb1.blue) ** 2
        )

    def _end_page(self, page: Page):
        vs: typing.List[typing.Tuple[Color, Decimal]] = [
            (k, v)
            for k, v in self._colors_from_palette_per_page[self._current_page].items()
        ]
        vs.sort(key=lambda x: x[1], reverse=True)
        self._colors_from_palette_per_page[self._current_page] = {
            k: v for k, v in vs[0 : self._max_number_of_colors_to_return]
        }

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, EndPageEvent):
            self._end_page(event.get_page())
        if isinstance(event, ChunkOfTextRenderEvent):
            self._render_text(event)
        if isinstance(event, ImageRenderEvent):
            self._render_image(event)

    @staticmethod
    def _get_rgb_from_image(img: PILImageModule.Image, x: int, y: int) -> RGBColor:
        c = img.getpixel((x, y))
        if img.mode == "RGB":
            return RGBColor(
                r=Decimal(c[0] / 255),
                g=Decimal(c[1] / 255),
                b=Decimal(c[2] / 255),
            )
        if img.mode == "RGBA":
            return RGBColor(
                r=Decimal(c[0] / 255),
                g=Decimal(c[1] / 255),
                b=Decimal(c[2] / 255),
            )
        if img.mode == "CMYK":
            r = int((1 - c[0]) * (1 - c[3]))
            g = int((1 - c[1]) * (1 - c[3]))
            b = int((1 - c[2]) * (1 - c[0]))
            return RGBColor(r=Decimal(r), g=Decimal(g), b=Decimal(b))
        return RGBColor(Decimal(0), Decimal(0), Decimal(0))

    @staticmethod
    def _nearest_color(c: Color, color_palette: typing.List[Color]) -> Color:
        c1: Color = color_palette[0]
        for c2 in color_palette:
            d1 = ColorExtraction._color_distance(c, c1)
            d2 = ColorExtraction._color_distance(c, c2)
            if d2 < d1:
                c1 = c2
        return c1

    def _render_image(self, event: ImageRenderEvent):
        r = (event.get_width() * event.get_height()) / (event.get_image().width * event.get_image().height)  # type: ignore[attr-defined]
        color_count: typing.Dict[RGBColor, Decimal] = {}
        for i in range(0, event.get_image().width):  # type: ignore [attr-defined]
            for j in range(0, event.get_image().height):  # type: ignore [attr-defined]
                c = ColorExtraction._get_rgb_from_image(event.get_image(), i, j)
                if c not in color_count:
                    color_count[c] = Decimal(1)
                else:
                    color_count[c] += Decimal(1)
        for k, v in color_count.items():
            self._update_color_count(v * r, k)

    def _render_text(self, event: ChunkOfTextRenderEvent):
        assert event is not None
        bb: typing.Optional[Rectangle] = event.get_previous_layout_box()
        s: Decimal = Decimal(0) if bb is None else (bb.width * bb.height)
        c: RGBColor = event.get_font_color().to_rgb()
        self._update_color_count(s, c)

    def _update_color_count(self, amount: Decimal, color: RGBColor):
        c2: Color = ColorExtraction._nearest_color(color, self._color_palette)
        self._colors_from_palette_per_page[self._current_page][c2] = (
            self._colors_from_palette_per_page[self._current_page].get(c2, Decimal(0))
            + amount
        )

    #
    # PUBLIC
    #

    def get_color(
        self,
    ) -> typing.Dict[int, typing.Dict[Color, Decimal]]:
        """
        This function returns the colors used on a given page of a PDF
        """
        return self._colors_from_palette_per_page

    @staticmethod
    def get_color_from_pdf(
        pdf: Document,
        max_number_of_colors_to_return: int = 32,
        max_number_of_colors_to_register: int = 32,
    ) -> typing.Dict[int, typing.Dict[Color, Decimal]]:
        """
        This function returns the colors used in a given PDF
        :param pdf:                                 the PDF to be analysed
        :param max_number_of_colors_to_return:      the maximum number of colors to return (i.e. "the top 10")
        :param max_number_of_colors_to_register:    the maximum number of colors to register (i.e. "do not distinguish between green and dark-green")
        :return:                                    the colors used in a given PDF
        """
        colors_per_page: typing.Dict[int, typing.Dict[Color, Decimal]] = {}
        number_of_pages: int = int(pdf.get_document_info().get_number_of_pages() or 0)
        for page_nr in range(0, number_of_pages):
            # get Page object
            page: Page = pdf.get_page(page_nr)
            page_source: io.BytesIO = io.BytesIO(page["Contents"]["DecodedBytes"])
            # register EventListener
            cse: "ColorExtraction" = ColorExtraction(
                max_number_of_colors_to_return=max_number_of_colors_to_return,
                max_number_of_colors_to_register=max_number_of_colors_to_register,
            )
            # process Page
            cse._event_occurred(BeginPageEvent(page))
            CanvasStreamProcessor(page, Canvas(), []).read(page_source, [cse])
            cse._event_occurred(EndPageEvent(page))
            # add to output dictionary
            colors_per_page[page_nr] = cse.get_color()[0]
        # return
        return colors_per_page
