#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class provides functions to extract a color palette (typing.List[Color]) from an Image
(specified by str, Path, borb Image, PIL Image)
"""
import math
import typing
from decimal import Decimal
import pathlib

from PIL import Image as PILImageModule

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.layout.image.image import Image as bImage


class ColorPaletteFromImage:
    """
    This class provides functions to extract a color palette (typing.List[Color]) from an Image
    (specified by str, Path, borb Image, PIL Image)
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _dist(c0: str, c1: str) -> float:
        r_delta = (int(c0[1:3], 16) - int(c1[1:3], 16)) ** 2 / (255 ** 2)
        g_delta = (int(c0[3:5], 16) - int(c1[3:5], 16)) ** 2 / (255 ** 2)
        b_delta = (int(c0[5:7], 16) - int(c1[5:7], 16)) ** 2 / (255 ** 2)
        return math.sqrt(r_delta + g_delta + b_delta) / math.sqrt(3)

    #
    # PUBLIC
    #

    @staticmethod
    def color_palette_from_image(
        img: typing.Union[str, pathlib.Path, bImage, PILImageModule.Image],
        limit: int = 4,
    ):
        """
        This function calculates the color palette from an Image
        :param img:     the input Image (specified by str, Path, borb Image, or PIL Image)
        :param limit:   the maximum number of colors in the palette
        :return:        a color palette (represented by typing.List[Color])
        """

        # convert everything to bImage
        if isinstance(img, str):
            img = bImage(img)
        if isinstance(img, pathlib.Path):
            img = bImage(img)
        if isinstance(img, PILImageModule.Image):
            img = bImage(img)
        assert isinstance(img, bImage)
        img.force_load_image()

        # resize
        assert isinstance(img.get_PIL_image(), PILImageModule.Image)
        img_in: PILImageModule.Image = img.get_PIL_image()
        while img_in.width > 128 and img_in.height > 128:
            img_in = img_in.resize((img_in.width // 2, img_in.height // 2))

        # get color histogram
        color_histogram: typing.Dict[str, int] = {}
        for x in range(0, img_in.width):
            for y in range(0, img_in.height):
                p: typing.Tuple[int, int, int] = img_in.getpixel((x, y))
                h: str = RGBColor(
                    Decimal(p[0] / 255.0), Decimal(p[1] / 255.0), Decimal(p[2] / 255.0)
                ).to_hex_string()
                color_histogram[h] = color_histogram.get(h, 0) + 1

        # compress color histogram
        sorted_histogram: typing.List[typing.Tuple[str, int]] = sorted(
            [(k, v) for k, v in color_histogram.items()],
            key=lambda x: x[1],
            reverse=True,
        )
        compressed_histogram: typing.List[typing.Tuple[str, int]] = []
        while len(sorted_histogram) > 0:
            # fmt: off
            c0, f0 = sorted_histogram[0]
            sorted_histogram.pop(0)
            similar_colors_and_frequencies = [t for t in sorted_histogram if ColorPaletteFromImage._dist(c0, t[0]) < 0.15 and t[1] < f0]
            similar_colors = [t[0] for t in similar_colors_and_frequencies]
            compressed_histogram += [(c0, f0 + sum([t[1] for t in similar_colors_and_frequencies] + [0]))]
            sorted_histogram = [t for t in sorted_histogram if t[0] not in similar_colors]
            # fmt: on

        # return
        colors_out: typing.List[HexColor] = [
            HexColor(x[0]) for x in compressed_histogram
        ]
        return colors_out[:limit]
