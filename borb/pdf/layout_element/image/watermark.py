#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a watermark to be applied to PDF documents, inheriting from the Image class.

This class is designed to handle the addition of watermarks (typically semi-transparent images or text) to PDF files.
It extends the functionality of the `Image` class, allowing for customization of watermark properties such as opacity,
size, and position.
"""
import io
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import name, stream


class Watermark(Image):
    """
    Represents a watermark to be applied to PDF documents, inheriting from the Image class.

    This class is designed to handle the addition of watermarks (typically semi-transparent images or text) to PDF files.
    It extends the functionality of the `Image` class, allowing for customization of watermark properties such as opacity,
    size, and position.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        text: str,
        angle_in_degrees: int = 45,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        font_color: Color = X11Color.RED,
        font_size: int = 24,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        transparency: float = 0.6,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a full-page watermark to be applied on the PDF.

        This constructor sets up the watermark text, its appearance, and its positioning
        across the entire page. You can customize the angle, font size, colors, margins,
        padding, and transparency to achieve the desired visual effect. The watermark
        will overlay the content of the PDF, making it suitable for branding or marking
        documents as confidential.

        :param text:                   The text to display as the watermark.
        :param angle_in_degrees:      The angle at which the watermark text is displayed (default is 45).
        :param background_color:       Optional background color for the watermark.
        :param border_color:           Optional border color for the watermark.
        :param border_dash_pattern:    Dash pattern used for the border lines of the watermark.
        :param border_dash_phase:      Phase offset for the dash pattern in the borders.
        :param border_width_bottom:    Width of the bottom border of the watermark.
        :param border_width_left:      Width of the left border of the watermark.
        :param border_width_right:     Width of the right border of the watermark.
        :param border_width_top:       Width of the top border of the watermark.
        :param font_color:             Color of the watermark text (default is RED).
        :param font_size:              Size of the watermark text (default is 24).
        :param horizontal_alignment:    Horizontal alignment of the watermark (default is LEFT).
        :param margin_bottom:          Space between the watermark and the element below it.
        :param margin_left:            Space between the watermark and the left page margin.
        :param margin_right:           Space between the watermark and the right page margin.
        :param margin_top:             Space between the watermark and the element above it.
        :param padding_bottom:         Padding inside the watermark at the bottom.
        :param padding_left:           Padding inside the watermark on the left side.
        :param padding_right:          Padding inside the watermark on the right side.
        :param padding_top:            Padding inside the watermark at the top.
        :param transparency:           Transparency level of the watermark (default is 0.6).
        :param vertical_alignment:      Vertical alignment of the watermark (default is TOP).
        """
        self.__text: str = text
        self.__font_size: int = font_size
        self.__transparency: float = transparency
        self.__font_color: Color = font_color
        self.__angle_in_degrees: int = angle_in_degrees

        # call super
        super().__init__(
            bytes_path_pil_image_or_url=Watermark.__create_watermark_image(
                text=text,
                font_size=font_size,
                transparency=transparency,
                font_color=font_color,
                angle_in_degrees=angle_in_degrees,
                size=(100, 100),
            )
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __create_watermark_image(
        size: typing.Tuple[int, int],
        text: str,
        angle_in_degrees: int = 45,
        font_color: Color = X11Color.RED,
        font_size: int = 24,
        transparency: float = 0.6,
    ):
        from PIL import Image as PILImageModule  # type: ignore[import-untyped, import-not-found]
        from PIL import ImageDraw, ImageFont  # type: ignore[import-untyped, import-not-found]

        # build new PIL.Image to hold text
        text_img: PILImageModule.Image = PILImageModule.new(
            mode="RGBA", size=(size[0], size[1]), color=(0, 0, 0, 0)
        )

        # determine hex representation of font color
        rgb_font_color: RGBColor = font_color.to_rgb_color()
        font_color_as_hex_str: str = "#"
        font_color_as_hex_str += hex(rgb_font_color.get_red())[2:].zfill(2).upper()
        font_color_as_hex_str += hex(rgb_font_color.get_green())[2:].zfill(2).upper()
        font_color_as_hex_str += hex(rgb_font_color.get_blue())[2:].zfill(2).upper()
        font_color_as_hex_str += hex(int(transparency * 255))[2:].zfill(2).upper()

        # draw text
        draw: ImageDraw.ImageDraw = ImageDraw.ImageDraw(text_img)
        draw.text(
            xy=(size[0] // 2, size[0] // 2),
            font=ImageFont.load_default(size=font_size),
            text=text,
            fill=font_color_as_hex_str,
            stroke_fill=font_color_as_hex_str,
        )

        # rotate
        text_img = text_img.rotate(
            angle=angle_in_degrees, center=(size[0] // 2, size[0] // 2)
        )

        # determine minimum dimensions of the (rotated) image_tests
        min_x: int = size[0]
        min_y: int = size[1]
        max_x: int = 0
        max_y: int = 0
        data = text_img.getdata()
        for y in range(0, size[1]):
            for x in range(0, size[0]):
                if data[y * size[0] + x] != (0, 0, 0, 0):
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        # crop text_image
        text_img = text_img.crop(box=(min_x, min_y, max_x, max_y))

        # return
        return text_img

    @staticmethod
    def __get_image_bytes(img) -> bytes:
        bytestream = io.BytesIO()
        img.save(bytestream, format="PNG")
        return bytestream.getvalue()

    #
    # PUBLIC
    #

    def get_size(
        self, available_space: typing.Tuple[int, int]
    ) -> typing.Tuple[int, int]:
        """
        Calculate and return the size of the layout element based on available space.

        This function uses the available space to compute the size (width, height)
        of the layout element in points.

        :param available_space: Tuple representing the available space (width, height).
        :return:                Tuple containing the size (width, height) in points.
        """
        return 0, 0

    def paint(
        self, available_space: typing.Tuple[int, int, int, int], page: Page
    ) -> None:
        """
        Render the layout element onto the provided page using the available space.

        This function renders the layout element within the given available space on the specified page.

        :param available_space: A tuple representing the available space (left, top, right, bottom).
        :param page:            The Page object on which to render the LayoutElement.
        :return:                None.
        """
        img = self.__create_watermark_image(
            text=self.__text,
            size=page.get_size(),
            transparency=self.__transparency,
            font_color=self.__font_color,
            angle_in_degrees=self.__angle_in_degrees,
        )
        self._LayoutElement__previous_paint_box = (
            0,
            0,
            page.get_size()[0],
            page.get_size()[1],
        )

        # resources
        if "Resources" not in page:
            page["Resources"] = {}
        if "XObject" not in page["Resources"]:
            page["Resources"]["XObject"] = {}

        # create new image_name
        image_name: str = "Im1"
        while image_name in page["Resources"]["XObject"]:
            image_name = f"Im{int(image_name[2:])+1}"
        page["Resources"]["XObject"][image_name] = img

        # Im (stream)
        image_stream: stream = stream()
        image_stream["Filter"] = name("DCTDecode")
        image_stream["Bytes"] = self.__get_image_bytes(img)
        image_stream["Type"] = name("XObject")
        image_stream["Subtype"] = name("Image")
        image_stream["Length"] = len(image_stream["Bytes"])
        image_stream["Width"] = img.width
        image_stream["Height"] = img.height
        image_stream["BitsPerComponent"] = 8
        image_stream["ColorSpace"] = name("DeviceRGB")
        page["Resources"]["XObject"][image_name] = image_stream

        # leading newline (if needed)
        Watermark._append_newline_to_content_stream(page)

        # store graphics state
        page["Contents"]["DecodedBytes"] += b"q\n"

        # write cm operator
        page["Contents"]["DecodedBytes"] += (
            f"{img.width} 0 "
            f"0 {img.height} "
            f"{page.get_size()[0]//2 - img.width//2} {page.get_size()[1]//2 - img.height//2} cm\n"
        ).encode("latin1")

        # write Do operator
        page["Contents"]["DecodedBytes"] += f"/{image_name} Do\n".encode("latin1")

        # restore graphics state
        page["Contents"]["DecodedBytes"] += b"Q\n"
