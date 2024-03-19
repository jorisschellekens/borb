#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This implementation of LayoutElement represents an Image
"""
import typing
from decimal import Decimal
import pathlib

import requests
from PIL import Image as PILImageModule

from borb.io.read.pdf_object import PDFObject
from borb.io.read.types import Dictionary
from borb.io.read.types import Name
from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.layout_element import LayoutElement
from borb.pdf.page.page import Page


class Image(LayoutElement):
    """
    This implementation of LayoutElement represents an Image
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        image: typing.Union[str, pathlib.Path, PILImageModule.Image],
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
        vertical_alignment: Alignment = Alignment.TOP,
        width: typing.Optional[Decimal] = None,
    ):
        super(Image, self).__init__(
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
            font="Helvetica",
            font_color=HexColor("#000000"),
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
        self._image: typing.Union[str, pathlib.Path, PILImageModule.Image] = image
        self._width: typing.Optional[Decimal] = width
        self._height: typing.Optional[Decimal] = height

    #
    # PRIVATE
    #

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        self.force_load_image()
        assert self._width is not None
        assert self._height is not None
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height() - self._height,
            self._width,
            self._height,
        )

    def _get_image_resource_name(self, image: PILImageModule, page: Page):  # type: ignore[valid-type]
        # create resources if needed
        if "Resources" not in page:
            page[Name("Resources")] = Dictionary().set_parent(page)
        if "XObject" not in page["Resources"]:
            page["Resources"][Name("XObject")] = Dictionary()

        # insert Image into resources
        self.force_load_image()
        image_resource_name: typing.Optional[Name] = next(
            iter([k for k, v in page["Resources"]["XObject"].items() if v == image]),
            None,
        )
        if image_resource_name is not None:
            return image_resource_name
        else:
            image_index = len(page["Resources"]["XObject"]) + 1
            page["Resources"]["XObject"][Name("Im%d" % image_index)] = image
            return Name("Im%d" % image_index)

    def _paint_content_box(self, page: Page, bounding_box: Rectangle):
        # add image to resources
        self.force_load_image()
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

    #
    # PUBLIC
    #

    def force_load_image(self) -> None:
        """
        This function forces the underlying PIL Image to load.
        Images can be specified by providing a Path, str, or PIL Image.
        The underlying image is only loaded when needed (such as when performing layout)
        :return:    None
        """
        # load Image from URL
        if isinstance(self._image, str):
            self._image = PILImageModule.open(
                requests.get(
                    self._image,
                    stream=True,
                    headers={
                        "Accept-Encoding": "",
                    },
                ).raw,
            )

        # load image
        if isinstance(self._image, pathlib.Path):
            self._image = PILImageModule.open(self._image)

        # self._image should be a PIL Image by now
        assert isinstance(self._image, PILImageModule.Image)
        # self._image = self._image.resize(size=(int(self._width), int(self._height)))
        PDFObject.add_pdf_object_methods(self._image)

        # set width / height
        if self._width is None:
            self._width = Decimal(self._image.width)
        if self._height is None:
            self._height = Decimal(self._image.height)

    def get_PIL_image(self) -> PILImageModule.Image:
        """
        This function returns the PIL.Image.Image underlying this borb Image
        :return:    the PIL.Image.Image underlying this borb Image
        """
        self.force_load_image()
        assert isinstance(self._image, PILImageModule.Image)
        return self._image
