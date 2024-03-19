#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This module contains all classes needed to apply OCR (using Tesseract) to a PDF document.
"""
import logging
import typing
from decimal import Decimal
import pathlib

from PIL import Image as PILImageModule
from PIL import ImageDraw

from borb.pdf.canvas.color.color import Color
from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.color.color import RGBColor
from borb.pdf.canvas.event.begin_page_event import BeginPageEvent
from borb.pdf.canvas.event.end_page_event import EndPageEvent
from borb.pdf.canvas.event.event_listener import Event
from borb.pdf.canvas.event.event_listener import EventListener
from borb.pdf.canvas.event.image_render_event import ImageRenderEvent
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.page.page import Page

logger = logging.getLogger(__name__)


class OCREvent(Event):
    """
    This implementation of Event represents content that was recognized during the OCR process.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        font: Font,
        font_size: Decimal,
        font_color: Color,
        bounding_box: Rectangle,
        page: Page,
        confidence: Decimal,
    ):
        self._text: str = text
        self._font: Font = font
        self._font_size: Decimal = font_size
        self._font_color: Color = font_color
        self._bounding_box: Rectangle = bounding_box
        self._page: Page = page
        self._confidence: Decimal = confidence

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_bounding_box(self) -> Rectangle:
        """
        This function returns the bounding box of this OCREvent
        """
        return self._bounding_box

    def get_confidence(self) -> Decimal:
        """
        This function returns the OCR confidence of this OCREvent
        """
        return self._confidence

    def get_font(self) -> Font:
        """
        This function returns the Font of this OCREvent.
        This will likely be an estimate of the actual Font used in the Image
        """
        return self._font

    def get_font_color(self) -> Color:
        """
        This function returns the font_color of this OCREvent
        """
        return self._font_color

    def get_font_size(self) -> Decimal:
        """
        This function returns the font_size of this OCREvent
        """
        return self._font_size

    def get_page(self) -> Page:
        """
        This function returns the Page of this OCREvent
        """
        return self._page

    def get_text(self) -> str:
        """
        This function returns the text of this OCREvent
        """
        return self._text


class OCRImageRenderEventListener(EventListener):
    """
    This implementation of EventListener attempts to perform OCR on Image objects inside a PDF.
    If text has been found, OCRImageRenderEventListener will add optional content to ensure
    the PDF can now be searched for the recognized text.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        tesseract_data_dir: pathlib.Path,
        minimal_confidence: Decimal = Decimal(0.75),
    ):
        # fmt: off
        assert tesseract_data_dir.exists(), "OCRImageRenderEventListener requires the tesseract data directory."
        assert tesseract_data_dir.is_dir(), "OCRImageRenderEventListener requires the tesseract data directory."
        # fmt: on

        self._tesseract_data_dir: pathlib.Path = tesseract_data_dir
        self._minimum_confidence: Decimal = minimal_confidence
        self._helvetica: Font = StandardType1Font("Helvetica")
        self._page: typing.Optional[Page] = None

    #
    # PRIVATE
    #

    def _event_occurred(self, event: Event) -> None:
        if isinstance(event, BeginPageEvent):
            self._page = event.get_page()
            return

        if isinstance(event, EndPageEvent):
            self._page = None
            return

        if isinstance(event, ImageRenderEvent):
            import pytesseract  # type: ignore[import]

            data = pytesseract.image_to_data(
                event.get_image(),
                lang="eng",
                config='--tessdata-dir "%s"' % str(self._tesseract_data_dir.absolute()),
                output_type=pytesseract.Output.DICT,
            )

            width_ratio: Decimal = event.get_width() / event.get_image().width
            height_ratio: Decimal = event.get_height() / event.get_image().height

            number_of_boxes: int = len(data["level"])
            for i in range(0, number_of_boxes):
                x: Decimal = Decimal(data["left"][i])
                # tesseract considers (LEFT, TOP) to be the origin
                # PDF prefers (LEFT, BOTTOM)
                # the following code fixes the mismatch
                y: Decimal = (
                    Decimal(event.get_image().height)
                    - Decimal(data["top"][i])
                    - Decimal(data["height"][i])
                )

                image_bounding_box: Rectangle = Rectangle(
                    x, y, Decimal(data["width"][i]), Decimal(data["height"][i])
                )

                # convert bounding box to Rectangle object
                pdf_bounding_box: Rectangle = Rectangle(
                    x * width_ratio + event.get_x(),
                    y * height_ratio + event.get_y(),
                    Decimal(data["width"][i]) * width_ratio,
                    Decimal(data["height"][i]) * height_ratio,
                )

                # get text in bounding box
                text_in_bounding_box: str = data["text"][i]
                if text_in_bounding_box.strip() == "":
                    continue

                # get confidence
                confidence: Decimal = Decimal(data["conf"][i])
                if confidence < self._minimum_confidence:
                    continue

                # delegate call
                assert self._page is not None
                font_size: Decimal = round(
                    self._get_font_size(
                        text_in_bounding_box, pdf_bounding_box.get_width()
                    ),
                    0,
                )
                font_color: Color = self._get_font_color(
                    text_in_bounding_box, event.get_image(), image_bounding_box
                )
                self._ocr_text_occurred(
                    OCREvent(
                        text_in_bounding_box,
                        self._helvetica,
                        font_size,
                        font_color,
                        pdf_bounding_box,
                        self._page,
                        confidence,
                    )
                )

    def _get_font_color(
        self,
        text: str,
        image: PILImageModule.Image,
        image_bounding_box: Rectangle,
    ) -> Color:
        # build empty PILImageModule
        text_image: PILImageModule.Image = PILImageModule.new(
            "RGB",
            (int(image_bounding_box.get_width()), int(image_bounding_box.get_height())),
            color=(255, 255, 255),
        )

        # write text
        # this can go wrong if the default font for drawing text
        # does not support one or more of the characters being drawn
        # in which case this code returns black
        try:
            text_image_draw = ImageDraw.Draw(text_image)
            text_image_draw.text((0, 0), text, fill=(0, 0, 0))
        except:
            logger.debug(
                "Unable to write '%s' in default PIL font. No metrics available to determine color. Defaulting to black."
                % text
            )
            return HexColor("000000")

        # count number of text pixels
        try:
            percentage_of_text_pixels: Decimal = Decimal(0)
            max_x: int = 0
            max_y: int = 0
            for i in range(0, text_image.width):
                for j in range(0, text_image.height):
                    if text_image.getpixel((i, j)) == (0, 0, 0):
                        percentage_of_text_pixels += Decimal(1)
                        max_x = max(max_x, i)
                        max_y = max(max_y, j)
            percentage_of_text_pixels /= Decimal(max_x * max_y)
        except:
            logger.debug(
                "Unable to obtain metrics to determine color. Defaulting to black."
            )
            return HexColor("000000")

        # crop image
        cropped_image = image.crop(
            (
                int(image_bounding_box.x),
                int(image.height - image_bounding_box.y - image_bounding_box.height),
                int(image_bounding_box.x + image_bounding_box.width),
                int(image.height - image_bounding_box.y),
            )
        )

        # count number of pixels in cropped image
        number_of_pixels_in_cropped_image: Decimal = Decimal(
            cropped_image.width * cropped_image.height
        )

        # build color histogram
        color_histogram: typing.Dict[str, Decimal] = {}
        for i in range(0, cropped_image.width):
            for j in range(0, cropped_image.height):
                color_tuple: typing.Tuple[int, int, int] = cropped_image.getpixel(
                    (i, j)
                )
                color_tuple = (
                    color_tuple[0] - color_tuple[0] % 16,
                    color_tuple[1] - color_tuple[1] % 16,
                    color_tuple[2] - color_tuple[2] % 16,
                )
                hex_color: str = RGBColor(
                    Decimal(color_tuple[0] / 255),
                    Decimal(color_tuple[1] / 255),
                    Decimal(color_tuple[2] / 255),
                ).to_hex_string()
                color_histogram[hex_color] = color_histogram.get(
                    hex_color, Decimal(0)
                ) + Decimal(1)

        # normalize
        color_histogram = {
            k: (v / number_of_pixels_in_cropped_image)
            for k, v in color_histogram.items()
        }

        # trim
        color_histogram = {k: v for k, v in color_histogram.items() if v > 0.05}

        # find best match
        min_delta: typing.Optional[Decimal] = None
        min_delta_color: typing.Optional[RGBColor] = None
        for k, v in color_histogram.items():
            delta: Decimal = abs(percentage_of_text_pixels - v)
            if min_delta is None or delta < min_delta:
                min_delta = delta
                min_delta_color = HexColor(k)

        # return
        return min_delta_color or HexColor("000000")

    def _get_font_size(self, text: str, bounding_box_width: Decimal) -> Decimal:
        """
        This function attempts to find the font_size that would best fit the given text in the given width
        :param text:                the text to fit
        :param bounding_box_width:  the bounding box (width) to fit
        """
        estimated_font_size_lowerbound: Decimal = Decimal(1)
        estimated_font_size_upperbound: Decimal = Decimal(1024)
        iteration_count: int = 0
        while (
            abs(estimated_font_size_upperbound - estimated_font_size_lowerbound) > 1
            and iteration_count < 11
        ):
            midpoint: Decimal = (
                estimated_font_size_upperbound + estimated_font_size_lowerbound
            ) / Decimal(2)
            midpoint = Decimal(int(midpoint))
            estimated_width: Decimal = self._get_text_width(midpoint, text)
            iteration_count += 1
            if estimated_width > bounding_box_width:
                estimated_font_size_upperbound = midpoint
                continue
            if estimated_width < bounding_box_width:
                estimated_font_size_lowerbound = midpoint
                continue
        return estimated_font_size_lowerbound

    def _get_text_width(self, font_size: Decimal, text: str):
        w: Decimal = Decimal(0)
        ZERO: Decimal = Decimal(0)
        for c in text:
            try:
                cid: typing.Optional[
                    int
                ] = self._helvetica.unicode_to_character_identifier(c)
                assert cid is not None
                w += (
                    (self._helvetica.get_width(cid) or ZERO)
                    * font_size
                    * Decimal(0.001)
                )
            except:
                pass
        return w

    def _ocr_text_occurred(self, event: OCREvent):
        pass

    #
    # PUBLIC
    #
