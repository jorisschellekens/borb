#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains everything needed to implement a LayoutElement representing a barcode.
"""
import typing
from decimal import Decimal
import enum

import barcode  # type: ignore[import]
import qrcode  # type: ignore[import]
from PIL import Image as PILImageModule

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment


class BarcodeType(enum.Enum):
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


class InMemoryBarcodeWriter(barcode.writer.ImageWriter):
    """
    This class inherits from BarcodeImageWriter, and enables
    access to the PILImageModule being built
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        super(InMemoryBarcodeWriter, self).__init__(format="JPEG", mode="RGB")
        self.output_image: typing.Optional[PILImageModule.Image] = None

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_output_image(self) -> PILImageModule.Image:  # type: ignore[valid-type]
        """
        This function returns the PIL.Image.Image representing the barcode
        :return:    the output PIL.Image.Image
        """
        assert self.output_image is not None
        return self.output_image

    def save(self, filename, output) -> None:
        """
        Saves the rendered output to `filename` storing the output.
        :param filename:    the filename (not used)
        :param output:      the rendered output
        :return:            None
        """
        self.output_image = output


class Barcode(Image):
    """
    This implementation of LayoutElement represents a barcode.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        data: str,
        type: BarcodeType,
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
        fill_color: Color = HexColor("ffffff"),
        height: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: Decimal = Decimal(0),
        margin_left: Decimal = Decimal(0),
        margin_right: Decimal = Decimal(0),
        margin_top: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        stroke_color: Color = HexColor("000000"),
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
            height=height,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            vertical_alignment=vertical_alignment,
            width=width,
        )
        self._background_color = fill_color

    #
    # PRIVATE
    #

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
        image: PILImageModule = writer.get_output_image()  # type: ignore[valid-type]
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
        png_image: PILImageModule = qr.make_image(  # type: ignore[valid-type]
            fill_color=self._stroke_color.to_rgb().to_hex_string(),
            back_color=self._fill_color.to_rgb().to_hex_string(),
        )
        jpg_image = png_image.convert("RGB")  # type: ignore [attr-defined]

        return jpg_image

    #
    # PUBLIC
    #
