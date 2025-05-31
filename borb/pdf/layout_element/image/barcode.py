#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a barcode image for embedding in a PDF document.

The Barcode class is designed to handle barcode images that can be embedded into a PDF document.
It inherits from the Image class, thus gaining all methods and attributes related to image handling in the PDF,
while adding specific functionality for encoding and displaying barcode data.
"""
import enum
import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class Barcode(Image):
    """
    Represents a barcode image for embedding in a PDF document.

    The Barcode class is designed to handle barcode images that can be embedded into a PDF document.
    It inherits from the Image class, thus gaining all methods and attributes related to image handling in the PDF,
    while adding specific functionality for encoding and displaying barcode data.
    """

    #
    # CONSTRUCTOR
    #

    class BarcodeType(enum.Enum):
        """
        Enumeration of various barcode formats supported by the PDF library.

        Each member of this enumeration represents a specific type of barcode,
        allowing users to select the appropriate barcode type when generating
        barcodes within a PDF document.
        """

        CODE_39 = 2
        CODE_128 = 3
        EAN_8 = 5
        EAN_13 = 7
        EAN_14 = 11
        ISBN_10 = 13
        ISBN_13 = 17
        ISSN = 19
        JAN = 23
        PZN = 29
        PZN_7 = 31
        UPCA = 37

    def __init__(
        self,
        barcode_data: str,
        barcode_type: BarcodeType,
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
        size: typing.Optional[typing.Tuple[int, int]] = None,
        stroke_color: Color = X11Color.BLACK,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize the Barcode object with the specified data and configuration.

        The `Barcode` class represents a barcode image generated from the provided
        data and type. This constructor initializes the barcode's attributes,
        including its visual appearance, layout properties, and specific barcode
        type. The barcode is designed to be rendered within a specified size,
        and it can accommodate various formatting options such as colors, borders,
        and alignment. This class inherits from the `Image` class, allowing it
        to be used as an image component in different layouts or documents.

        :param barcode_data:            A string containing the data to be encoded in the barcode.
        :param barcode_type:            An instance of `BarcodeType` that specifies the type of barcode to be generated (e.g., QR Code, UPC, EAN).
        :param background_color:        An optional color for the barcode's background. Defaults to white (X11Color.WHITE).
        :param border_color:            An optional color for the barcode's border. Defaults to None (no border).
        :param border_dash_pattern:     A list of integers representing the dash pattern for the border (if applicable). Defaults to an empty  list (solid line).
        :param border_dash_phase:       An integer that specifies the phase offset of the dashed border pattern. Defaults to 0.
        :param border_width_bottom:     The width of the bottom border. Defaults to 0.
        :param border_width_left:       The width of the left border. Defaults to 0.
        :param border_width_right:      The width of the right border. Defaults to 0.
        :param border_width_top:        The width of the top border. Defaults to 0.
        :param horizontal_alignment:    An instance of `LayoutElement.HorizontalAlignment` that determines the horizontal alignment of the barcode. Defaults to left alignment.
        :param margin_bottom:           The bottom margin for the barcode layout. Defaults to 0.
        :param margin_left:             The left margin for the barcode layout. Defaults to 0.
        :param margin_right:            The right margin for the barcode layout. Defaults to 0.
        :param margin_top:              The top margin for the barcode layout. Defaults to 0.
        :param padding_bottom:          The bottom padding within the barcode layout. Defaults to 0.
        :param padding_left:            The left padding within the barcode layout. Defaults to 0.
        :param padding_right:           The right padding within the barcode layout. Defaults to 0.
        :param padding_top:             The top padding within the barcode layout. Defaults to 0.
        :param stroke_color:            The color of the barcode's bars. Defaults to black (X11Color.BLACK).
        :param size:                    An optional tuple specifying the width and height of the barcode image.
        :param vertical_alignment:      An instance of `LayoutElement.VerticalAlignment` that determines the vertical alignment of the barcode. Defaults to top alignment.
        """
        super().__init__(
            bytes_path_pil_image_or_url=Barcode.__get_image(
                barcode_data=barcode_data,
                barcode_type=barcode_type,
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
            size=size,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __get_image(
        barcode_data: str,
        barcode_type: BarcodeType,
        size: typing.Tuple[int, int],
        background_color: Color = X11Color.WHITE,
        stroke_color: Color = X11Color.BLACK,
    ) -> "PIL.Image.Image":  # type: ignore[name-defined]

        # determine raw modules using barcode library
        modules: typing.List[bool] = []
        if barcode_type == Barcode.BarcodeType.CODE_39:
            try:
                from barcode import Code39  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in Code39(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.CODE_128:
            try:
                from barcode import Code128  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in Code128(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.EAN_8:
            try:
                from barcode import EAN8  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in EAN8(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.EAN_13:
            try:
                from barcode import EAN13  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in EAN13(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.EAN_14:
            try:
                from barcode import EAN14  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in EAN14(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.ISBN_10:
            try:
                from barcode import ISBN10  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in ISBN10(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.ISBN_13:
            try:
                from barcode import ISBN13  # type: ignore[import-untyped]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in ISBN13(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.ISSN:
            try:
                from barcode import ISSN  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in ISSN(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.JAN:
            try:
                from barcode import JAN  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in JAN(barcode_data).build()[0]]
        elif barcode_type in [Barcode.BarcodeType.PZN, Barcode.BarcodeType.PZN_7]:
            try:
                from barcode import PZN  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in PZN(barcode_data).build()[0]]
        elif barcode_type == Barcode.BarcodeType.UPCA:
            try:
                from barcode import UPCA  # type: ignore[import-untyped, import-not-found]
            except ImportError:
                raise ImportError(
                    "Please install the 'barcode' library to use the Barcode class. "
                    "You can install it with 'pip install python-barcode'."
                )

            modules = [(d == "1") for d in UPCA(barcode_data).build()[0]]

        # calculate the best width (a multiple of the number of modules)
        best_width: int = math.ceil(size[0] / len(modules)) * len(modules)
        module_width: int = int(best_width // len(modules))

        rgb_background_color: RGBColor = background_color.to_rgb_color()

        try:
            import PIL.Image  # type: ignore[import-untyped, import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'Pillow' library to use the Barcode class. "
                "You can install it with 'pip install Pillow'."
            )
        img = PIL.Image.new(
            mode="RGB",
            size=(best_width, size[1]),
            color=(
                rgb_background_color.get_red(),
                rgb_background_color.get_green(),
                rgb_background_color.get_blue(),
            ),
        )

        # draw modules
        rgb_stroke_color: RGBColor = stroke_color.to_rgb_color()
        pixels = img.load()
        assert pixels is not None
        for i, module_value in enumerate(modules):
            if not module_value:
                continue
            for j in range(i * module_width, (i + 1) * module_width):
                for k in range(img.size[1]):
                    pixels[j, k] = (
                        rgb_stroke_color.get_red(),
                        rgb_stroke_color.get_green(),
                        rgb_stroke_color.get_blue(),
                    )

        # return
        return img

    #
    # PUBLIC
    #
