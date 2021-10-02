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
        width: Optional[Decimal] = None,
        height: Optional[Decimal] = None,
        margin_top: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        if isinstance(image, str):
            image = PILImage.open(
                requests.get(
                    image,
                    stream=True,
                ).raw
            )
        if isinstance(image, Path):
            image = PILImage.open(image)
        super(Image, self).__init__(
            font_size=Decimal(12),
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
            margin_top=margin_top or Decimal(5),
            margin_right=margin_right or Decimal(5),
            margin_bottom=margin_bottom or Decimal(5),
            margin_left=margin_left or Decimal(5),
        )
        add_base_methods(image)
        self._image: PILImage = image
        self._width = width or Decimal(self._image.width)
        self._height = height or Decimal(self._image.height)

    def _get_image_resource_name(self, image: PILImage, page: Page):
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

    def _calculate_layout_box_without_padding(
        self, page: "Page", bounding_box: Rectangle  # type: ignore[name-defined]
    ) -> Rectangle:

        # return
        layout_box: Rectangle = Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.get_height() - self._height,
            self._width,
            self._height,
        )
        self.set_bounding_box(layout_box)
        return layout_box

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # add image to resources
        image_resource_name = self._get_image_resource_name(self._image, page)

        assert self._width is not None
        assert self._height is not None

        # write Do operator
        content = " q %f 0 0 %f %f %f cm /%s Do Q " % (
            self._width,
            self._height,
            bounding_box.get_x(),
            bounding_box.get_y() + bounding_box.get_height() - self._height,
            image_resource_name,
        )

        # write content
        self._append_to_content_stream(page, content)

        # return
        return Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.get_height() - self._height,
            self._width,
            self._height,
        )
