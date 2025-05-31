#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a QR code image that can be embedded in a PDF document.

The `QRCode` class is designed to represent QR code images that can be embedded into a
PDF document. Since it inherits from the `Image` class, it inherits all methods and
attributes related to image handling in the PDF, while adding specific functionality
for encoding and displaying QR code data.
"""
import enum
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class QRCode(Image):
    """
    Represents a QR code image that can be embedded in a PDF document.

    The `QRCode` class is designed to represent QR code images that can be embedded into a
    PDF document. Since it inherits from the `Image` class, it inherits all methods and
    attributes related to image handling in the PDF, while adding specific functionality
    for encoding and displaying QR code data.
    """

    class QRCodeType(enum.Enum):
        """
        The QRCodeType class is an enumeration that defines the various barcode formats supported by the PDF library.

        Each member of this enumeration represents a specific type of qr code,
        allowing users to select the correct barcode type when generating qr codes within the PDF.
        """

        MICRO = 2
        REGULAR = 3

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        qr_code_data: str,
        background_color: typing.Optional[Color] = X11Color.WHITE,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        qr_code_type: QRCodeType = QRCodeType.REGULAR,
        size: typing.Optional[typing.Tuple[int, int]] = None,
        stroke_color: Color = X11Color.BLACK,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a QR code object with specific layout and styling options.

        This constructor creates a QR code based on the provided `qr_code_data`, along with
        additional customization options like the QR code type, border properties, alignment,
        margins, padding, and more. It allows for flexible control over how the QR code will
        be displayed within a PDF layout.

        :param qr_code_data:            The data to be encoded within the QR code, typically a string representing a URL, text, or other information.
        :param qr_code_type:            The type of QR code to generate, such as `QRCodeType.REGULAR`. Defaults to `QRCodeType.REGULAR`.
        :param background_color:        The background color of the QR code. Defaults to white.
        :param border_color:            The color of the border around the QR code, if any.
        :param border_dash_pattern:     A list of integers defining the dash pattern of the border.
        :param border_dash_phase:       The phase offset for the dash pattern of the border.
        :param border_width_bottom:     The width of the bottom border.
        :param border_width_left:       The width of the left border.
        :param border_width_right:      The width of the right border.
        :param border_width_top:        The width of the top border.
        :param horizontal_alignment:    Specifies how the QR code should be horizontally aligned within its container.
        :param margin_bottom:           The bottom margin around the QR code.
        :param margin_left:             The left margin around the QR code.
        :param margin_right:            The right margin around the QR code.
        :param margin_top:              The top margin around the QR code.
        :param padding_bottom:          The bottom padding inside the QR code container.
        :param padding_left:            The left padding inside the QR code container.
        :param padding_right:           The right padding inside the QR code container.
        :param padding_top:             The top padding inside the QR code container.
        :param size:                    The size of the QR code in (width, height) format. If not provided, the size will be automatically calculated based on the content.
        :param stroke_color:            The color used to draw the QR code.
        :param vertical_alignment:      Specifies how the QR code should be vertically aligned within its container.
        """
        super().__init__(
            bytes_path_pil_image_or_url=QRCode.__get_image(
                qr_code_data=qr_code_data,
                qr_code_type=qr_code_type,
                size=size or (134, 134),
                stroke_color=stroke_color,
                background_color=background_color or X11Color.WHITE,
            ),
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_top=border_width_top,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            background_color=background_color,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            padding_right=padding_right,
            padding_top=padding_top,
            size=size or (134, 134),
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __get_image(
        qr_code_data: str,
        qr_code_type: QRCodeType,
        size: typing.Tuple[int, int],
        background_color: Color = X11Color.WHITE,
        stroke_color: Color = X11Color.BLACK,
    ) -> "PIL.Image.Image":  # type: ignore[name-defined]
        try:
            import segno  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'segno' library to use the QRCode class. "
                "You can install it with 'pip install segno'."
            )

        if qr_code_type == QRCode.QRCodeType.MICRO:
            qr = segno.make_micro(content=qr_code_data)
        else:
            qr = segno.make_qr(content=qr_code_data)

        data = [[(col == 1) for col in row] for row in qr.matrix_iter()]

        while not any(data[0]):
            data = data[1:]
        while not any(data[-1]):
            data = data[:-1]
        while not any(row[0] for row in data):
            data = [row[1:] for row in data]
        while not any(row[-1] for row in data):
            data = [row[:-1] for row in data]

        # calculate best width (a multiple of the number of bars)
        rows: int = len(data)
        cols: int = len(data[0])
        best_width: int = math.ceil(size[0] / rows) * rows
        best_height: int = math.ceil(size[1] // cols) * cols

        # calculate the width/height of a single module
        module_width: int = int(best_width // rows)
        module_height: int = int(best_height // cols)
        module_width = max(module_width, module_height)
        module_height = module_width

        # re-calculate best_width, best_height
        best_width = rows * module_width
        best_height = cols * module_height

        # build image_tests
        try:
            import PIL.Image  # type: ignore[import-untyped, import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'Pillow' library to use the QRCode class. "
                "You can install it with 'pip install Pillow'."
            )

        rgb_background_color: RGBColor = background_color.to_rgb_color()
        img = PIL.Image.new(
            mode="RGB",
            size=(best_width, best_height),
            color=(
                rgb_background_color.get_red(),
                rgb_background_color.get_green(),
                rgb_background_color.get_blue(),
            ),
        )

        # start filling in the code
        rgb_stroke_color: RGBColor = stroke_color.to_rgb_color()
        pixels = img.load()
        assert pixels is not None
        for i in range(rows):
            for j in range(cols):
                if not data[i][j]:
                    continue
                for k in range(0, module_width):
                    for l in range(0, module_height):
                        if data[i][j]:
                            pixels[i * module_width + k, j * module_height + l] = (
                                rgb_stroke_color.get_red(),
                                rgb_stroke_color.get_green(),
                                rgb_stroke_color.get_blue(),
                            )

        # return
        return img

    #
    # PUBLIC
    #
