#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A watermark is an identifying image or pattern in paper that appears as various shades of lightness/darkness when viewed
by transmitted light (or when viewed by reflected light, atop a dark background), caused by thickness or density variations in the paper.

Watermarks have been used on postage stamps, currency, and other government documents to discourage counterfeiting.
There are two main ways of producing watermarks in paper; the dandy roll process, and the more complex cylinder mould process.

Watermarks vary greatly in their visibility; while some are obvious on casual inspection,
others require some study to pick out. Various aids have been developed, such as watermark fluid that wets the paper without damaging it.

A watermark is very useful in the examination of paper because it can be used for dating documents and artworks,
identifying sizes, mill trademarks and locations, and determining the quality of a sheet of paper.

The word is also used for digital practices that share similarities with physical watermarks.
In one case, overprint on computer-printed output may be used to identify output from an unlicensed trial version of a program.
In another instance, identifying codes can be encoded as a digital watermark for a music, video, picture, or other file.
"""
import typing
from decimal import Decimal
import pathlib

from PIL import Image as PILImageModule
from PIL import ImageDraw
from PIL import ImageFont

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.page.page import Page


class Watermark(Image):
    """
    A watermark is an identifying image or pattern in paper that appears as various shades of lightness/darkness when viewed
    by transmitted light (or when viewed by reflected light, atop a dark background), caused by thickness or density variations in the paper.

    Watermarks have been used on postage stamps, currency, and other government documents to discourage counterfeiting.
    There are two main ways of producing watermarks in paper; the dandy roll process, and the more complex cylinder mould process.

    Watermarks vary greatly in their visibility; while some are obvious on casual inspection,
    others require some study to pick out. Various aids have been developed, such as watermark fluid that wets the paper without damaging it.

    A watermark is very useful in the examination of paper because it can be used for dating documents and artworks,
    identifying sizes, mill trademarks and locations, and determining the quality of a sheet of paper.

    The word is also used for digital practices that share similarities with physical watermarks.
    In one case, overprint on computer-printed output may be used to identify output from an unlicensed trial version of a program.
    In another instance, identifying codes can be encoded as a digital watermark for a music, video, picture, or other file.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        angle_in_degrees: float = 45,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        font_color: Color = HexColor("000000"),
        font_size: Decimal = Decimal(30),
        height: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        transparency: float = 0.6,
        vertical_alignment: Alignment = Alignment.TOP,
        width: typing.Optional[Decimal] = None,
    ):
        assert 1 <= len(text) <= 64
        assert 0 < transparency <= 1
        super(Watermark, self).__init__(
            image=Watermark._get_watermark_image(
                text,
                angle_in_degrees=angle_in_degrees,
                font_color_as_hex_str=font_color.to_rgb().to_hex_string(),
                font_size=int(font_size),
                height=height,
                transparency=transparency,
                width=width,
            ),
            background_color=background_color,
            border_bottom=border_bottom,
            border_color=border_color,
            border_left=border_left,
            border_radius_bottom_left=border_radius_bottom_left,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_right=border_right,
            border_top=border_top,
            border_width=border_width,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom if margin_bottom is not None else Decimal(5),
            margin_left=margin_left if margin_left is not None else Decimal(5),
            margin_right=margin_right if margin_right is not None else Decimal(5),
            margin_top=margin_top if margin_top is not None else Decimal(5),
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    @staticmethod
    def _get_font_path() -> typing.Optional[pathlib.Path]:

        # find system font(s)
        potential_fonts: typing.List[pathlib.Path] = [
            pathlib.Path("/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf")
        ]
        for x in potential_fonts:
            if x.exists():
                return x

        # default
        return None

    @staticmethod
    def _get_watermark_image(
        s: str,
        angle_in_degrees: float = 45,
        font_color_as_hex_str: str = "#000000",
        font_size: int = 12,
        height: typing.Optional[Decimal] = None,
        transparency: float = 0.5,
        width: typing.Optional[Decimal] = None,
    ) -> PILImageModule.Image:

        # build new PIL.Image to hold text
        W: int = int(width or Decimal(595))
        H: int = int(height or Decimal(842))
        text_img: PILImageModule.Image = PILImageModule.new(mode="RGBA", size=(W, H))

        # convert transparency to hex
        transparency_hex: str = hex(255 - int(transparency * 255))[2:]

        # draw text
        draw: ImageDraw.ImageDraw = ImageDraw.ImageDraw(text_img)
        font_path: typing.Optional[pathlib.Path] = Watermark._get_font_path()
        font: typing.Optional[
            typing.Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]
        ] = None
        if font_path is not None:
            font = ImageFont.truetype(str(font_path), size=font_size)
            scale_factor: float = 1
        else:
            font = ImageFont.load_default()
            scale_factor = (font_size / font.getsize("x")[0]) * 0.6
        assert font is not None

        draw.text(
            xy=(W // 2, H // 2),
            font=font,
            text=s,
            fill=font_color_as_hex_str + transparency_hex,
            stroke_fill=font_color_as_hex_str + transparency_hex,
        )

        # rotate
        text_img = text_img.rotate(angle=angle_in_degrees, center=(W // 2, H // 2))

        # determine minimum dimensions of the (rotated) image
        min_x: int = W
        min_y: int = H
        max_x: int = 0
        max_y: int = 0
        data = text_img.getdata()
        for y in range(0, H):
            for x in range(0, W):
                if data[y * W + x] != (0, 0, 0, 0):
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        # crop the text_image
        w: int = max_x - min_x
        h: int = max_y - min_y
        text_img = text_img.crop(box=(min_x, min_y, max_x, max_y))

        # scale (if needed)
        if scale_factor != 1:
            w = int(w * scale_factor)
            h = int(h * scale_factor)
            text_img = text_img.resize(size=(w, h), resample=PILImageModule.LANCZOS)

        # create background_img
        background_img = PILImageModule.new(mode="RGBA", size=(W, H))

        # paste text_img on background_img
        for y in range(0, h):
            for x in range(0, w):
                background_img.putpixel(
                    xy=(x + W // 2 - w // 2, y + H // 2 - h // 2),
                    value=text_img.getpixel(xy=(x, y)),
                )

        # return
        return background_img

    #
    # PUBLIC
    #

    def paint(self, page: "Page", available_space: Rectangle) -> None:
        """
        This method paints this LayoutElement on the given Page, in the available space
        :param page:                the Page on which to paint this LayoutElement
        :param available_space:     the available space (as a Rectangle) on which to paint this LayoutElement
        :return:                    None
        """
        W: int = int(page.get_page_info().get_width() or Decimal(595))
        H: int = int(page.get_page_info().get_height() or Decimal(842))
        w: int = self.get_PIL_image().width
        h: int = self.get_PIL_image().height
        super().paint(
            page,
            Rectangle(
                Decimal(W // 2 - w // 2),
                Decimal(H // 2 - h // 2),
                Decimal(w),
                Decimal(h),
            ),
        )
