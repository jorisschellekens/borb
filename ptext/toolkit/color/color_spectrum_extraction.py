#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This implementation of EventListener  extracts the colors used in rendering a PDF
"""
import typing
from decimal import Decimal
from typing import Optional

from PIL.Image import Image  # type: ignore [import]

from ptext.pdf.canvas.color.color import RGBColor
from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.chunk_of_text_render_event import ChunkOfTextRenderEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.canvas.event.image_render_event import ImageRenderEvent
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.page.page import Page


class ColorSpectrumExtraction(EventListener):
    """
    This implementation of EventListener  extracts the colors used in rendering a PDF
    """

    def __init__(self, maximum_number_of_colors: Optional[int] = None):
        """
        Constructs a new ColorSpectrumExtraction
        """
        self.maximum_number_of_colors = 64
        if maximum_number_of_colors is not None:
            self.maximum_number_of_colors = maximum_number_of_colors
        self.colors_per_page: typing.Dict[
            int, typing.Dict[typing.Tuple[int, int, int], int]
        ] = {}
        self.current_page = -1

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event.get_page())
        if isinstance(event, ChunkOfTextRenderEvent):
            self._render_text(event)
        if isinstance(event, ImageRenderEvent):
            self._render_image(event)

    def _begin_page(self, page: Page):
        self.current_page += 1
        self.colors_per_page[self.current_page] = {}

    def _render_text(self, event: ChunkOfTextRenderEvent):
        assert event is not None
        bb: typing.Optional[Rectangle] = event.get_bounding_box()
        s = 0 if bb is None else int(bb.width * bb.height)
        c = event.font_color.to_rgb()
        self._register_color(s, c)

    def _render_image(self, event: ImageRenderEvent):
        r = (event.get_width() * event.get_height()) / (
            event.get_image().width * event.get_image().height
        )
        color_count: typing.Dict[RGBColor, Decimal] = {}
        for i in range(0, event.get_image().width):
            for j in range(0, event.get_image().height):
                c = ColorSpectrumExtraction._get_rgb_from_image(event.get_image(), i, j)
                if c not in color_count:
                    color_count[c] = Decimal(1)
                else:
                    color_count[c] += Decimal(1)
        for k, v in color_count.items():
            self._register_color(int(v * r), k)

    @staticmethod
    def _get_rgb_from_image(img: Image, x: int, y: int) -> RGBColor:
        c = img.getpixel((x, y))
        if img.mode == "RGB":
            return RGBColor(r=Decimal(c[0]), g=Decimal(c[1]), b=Decimal(c[2]))
        if img.mode == "RGBA":
            return RGBColor(r=Decimal(c[0]), g=Decimal(c[1]), b=Decimal(c[2]))
        if img.mode == "CMYK":
            r = int((1 - c[0]) * (1 - c[3]) / 255)
            g = int((1 - c[1]) * (1 - c[3]) / 255)
            b = int((1 - c[2]) * (1 - c[0]) / 255)
            return RGBColor(r=Decimal(r), g=Decimal(g), b=Decimal(b))
        return RGBColor(Decimal(0), Decimal(0), Decimal(0))

    def _register_color(self, amount: int, color: RGBColor):
        mod_step = int(256 / (self.maximum_number_of_colors ** (1.0 / 3)))
        r = int(color.to_rgb().red)
        r = r - r % mod_step

        g = int(color.to_rgb().green)
        g = g - g % mod_step

        b = int(color.to_rgb().blue)
        b = b - b % mod_step

        t = (r, g, b)
        if t not in self.colors_per_page[self.current_page]:
            self.colors_per_page[self.current_page][t] = amount
        else:
            self.colors_per_page[self.current_page][t] += amount

    def get_colors_per_page(
        self, page_number: int, limit: Optional[int] = None
    ) -> typing.List[RGBColor]:
        """
        This function returns the colors used on a given page of a PDF
        """
        if limit is None:
            limit = 32
        tmp = sorted(
            [
                (RGBColor(Decimal(k[0]), Decimal(k[1]), Decimal(k[2])), int(v))
                for k, v in self.colors_per_page[page_number].items()
            ],
            key=lambda x: x[1],
        )[-limit:]
        return tmp
