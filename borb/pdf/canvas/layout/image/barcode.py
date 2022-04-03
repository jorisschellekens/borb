#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains everything needed to implement a LayoutElement representing a barcode.
"""
import typing
from decimal import Decimal
from enum import Enum

import barcode  # type: ignore [import]
import qrcode  # type: ignore [import]
from barcode.writer import ImageWriter as BarcodeImageWriter  # type: ignore [import]
from PIL import Image as PILImage  # type: ignore [import]

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment


class BarcodeType(Enum):
    """
    This Enum represents the various types of supported barcodes
    """

    CODE_128 = "code128"
    CODE_39 = "code39"
    EAN = "ean"
    EAN_13 = "ean13"
    EAN_14 = "ean14"
    EAN_8 = "ean8"
    GS_1 = "isbn13"
    GS_128 = "gs1_128"
    GTIN = "ean14"
    ISBN = "isbn13"
    ISBN_10 = "isbn10"
    ISBN_13 = "isbn13"
    ISSN = "issn"
    ITF = "itf"
    JAN = "jan"
    PZN = "pzn"
    QR = "qr"
    UPC = "upca"
    UPC_A = "upca"


class InMemoryBarcodeWriter(BarcodeImageWriter):
    """
    This class inherits from BarcodeImageWriter, and enables
    access to the PILImage being built
    """

    def __init__(self):
        super(InMemoryBarcodeWriter, self).__init__(format="JPEG", mode="RGB")
        self.output_image: typing.Optional[PILImage] = None

    def save(self, filename, output):
        """
        Saves the rendered output to `filename` storing the output.

        :parameters:
            filename : String
                Filename without extension.
            output : String
                The rendered output.

        :returns: The full filename with extension.
        :rtype: String
        """
        self.output_image = output

    def get_output_image(self) -> PILImage:
        """
        This function returns the PILImage representing the barcode
        """
        return self.output_image


class Barcode(Image):
    """
    This implementation of LayoutElement represents a barcode.
    """

    def __init__(
        self,
        data: str,
        type: BarcodeType,
        stroke_color: Color = HexColor("000000"),
        fill_color: Color = HexColor("ffffff"),
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
        self._data: str = data
        self._type: BarcodeType = type
        self._stroke_color: Color = stroke_color
        self._fill_color: Color = fill_color

        assert stroke_color != fill_color

        if type == BarcodeType.QR:
            image = self._generate_qr_code(data)
        else:
            image = self._generate_image_except_qr_code(data, type)

        # call to super
        super(Barcode, self).__init__(
            image,
            width=width,
            height=height,
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
            margin_bottom=margin_bottom or Decimal(5),
            margin_left=margin_left or Decimal(5),
            margin_right=margin_right or Decimal(5),
            margin_top=margin_top or Decimal(5),
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
        )
        self._background_color = fill_color

    def _generate_image_except_qr_code(self, data: str, type: BarcodeType):
        # generate image using barcode library
        writer: InMemoryBarcodeWriter = InMemoryBarcodeWriter()
        ean = barcode.get(name=type.value, code=data, writer=writer)
        ean.save(
            "",
            options={
                "foreground": self._stroke_color.to_rgb().to_hex_string(),
                "background": self._fill_color.to_rgb().to_hex_string(),
            },
        )

        # get the rendered image from InMemoryBarcodeWriter
        image: PILImage = writer.get_output_image()
        assert image is not None
        assert image.width > 0
        assert image.height > 0

        # return
        return image

    def _generate_qr_code(self, data: str):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # png to jpg
        png_image: PILImage = qr.make_image(
            fill_color=self._stroke_color.to_rgb().to_hex_string(),
            back_color=self._fill_color.to_rgb().to_hex_string(),
        )
        jpg_image = png_image.convert("RGB")

        return jpg_image
