#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an Image
"""
import typing
from decimal import Decimal
from pathlib import Path
from typing import Optional

import requests
from PIL import Image as PILImage  # type: ignore [import]

from borb.io.read.types import Dictionary, Name, add_base_methods
from borb.pdf.canvas.color.color import HexColor, Color
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment, LayoutElement
from borb.pdf.page.page import Page


class Image(LayoutElement):
    """
    This implementation of LayoutElement represents an Image
    """

    def __init__(
        self,
        image: typing.Union[str, Path, PILImage.Image],
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
        height: Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        vertical_alignment: Alignment = Alignment.TOP,
        width: Optional[Decimal] = None,
    ):
        if isinstance(image, str):
            image = PILImage.open(
                requests.get(
                    image,
                    stream=True,
                    headers={
                        "Accept-Encoding": "",
                    },
                ).raw,
            )
        if isinstance(image, Path):
            image = PILImage.open(image)
        super(Image, self).__init__(
            background_color=None,
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
            font_size=Decimal(12),
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
        add_base_methods(image)
        self._image: PILImage = image  # type: ignore[valid-type]
        self._width = width or Decimal(self._image.width)
        self._height = height or Decimal(self._image.height)

    def _get_image_resource_name(self, image: PILImage, page: Page):  # type: ignore[valid-type]
        # create resources if needed
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary().set_parent(page)  # type: ignore [attr-defined]
        if "XObject" not in page["Resources"]:
            page["Resources"][Name("XObject")] = Dictionary()

        # insert font into resources
        image_resource_name = [
            k for k, v in page["Resources"]["XObject"].items() if v == image
        ]
        if len(image_resource_name) > 0:
            return image_resource_name[0]
        else:
            image_index = len(page["Resources"]["XObject"]) + 1
            page["Resources"]["XObject"][Name("Im%d" % image_index)] = image
            return Name("Im%d" % image_index)

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - self._height,
            self._width,
            self._height,
        )

    def _paint_content_box(self, page: Page, bounding_box: Rectangle):

        # add image to resources
        image_resource_name = self._get_image_resource_name(self._image, page)

        assert self._width is not None
        assert self._height is not None

        # write Do operator
        content = " q %f 0 0 %f %f %f cm /%s Do Q " % (
            float(self._width),
            float(self._height),
            float(bounding_box.get_x()),
            float(bounding_box.get_y() + bounding_box.get_height() - self._height),
            image_resource_name,
        )

        # write content
        page.append_to_content_stream(content)
