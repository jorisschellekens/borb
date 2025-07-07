#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an image that can be embedded in a PDF layout.

The `Image` class provides flexible options for specifying an image source. The image
can be supplied through a URL, image bytes, a `pathlib.Path`, or a `PIL.Image`
object. This class allows for seamless integration of images into PDF layouts.
"""
import io
import pathlib
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import name, stream


class Image(LayoutElement):
    """
    Represents an image that can be embedded in a PDF layout.

    The `Image` class provides flexible options for specifying an image source. The image
    can be supplied through a URL, image bytes, a `pathlib.Path`, or a `PIL.Image`
    object. This class allows for seamless integration of images into PDF layouts.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        bytes_path_pil_image_or_url: typing.Union[  # type: ignore[name-defined]
            bytes, pathlib.Path, "PIL.Image.Image", str  # type: ignore[name-defined]
        ],
        background_color: typing.Optional[Color] = None,
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
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize an Image object for use in a PDF document.

        The `Image` class represents an image that can be added to a PDF document. This constructor allows
        the user to specify the source of the image in various formats (bytes, file path, PIL image, or URL),
        along with a range of styling options such as background color, borders, alignment, and size. The
        image can be positioned with customizable margins and padding.

        :param bytes_path_pil_image_or_url: The image source, which can be provided as raw bytes,
                                            a file path (`pathlib.Path`),
                                            a PIL image object (`PIL.Image`),
                                            or a URL as a string.
        :param background_color:            The background color behind the image (optional).
        :param border_color:                The color of the image's border (optional).
        :param border_dash_pattern:         A list of integers defining the dash pattern for the border (default is solid).
        :param border_dash_phase:           The phase of the dash pattern for the border (default is 0).
        :param border_width_bottom:         The width of the bottom border (default is 0).
        :param border_width_left:           The width of the left border (default is 0).
        :param border_width_right:          The width of the right border (default is 0).
        :param border_width_top:            The width of the top border (default is 0).
        :param horizontal_alignment:        The horizontal alignment of the image (default is left-aligned).
        :param margin_bottom:               The margin below the image (default is 0).
        :param margin_left:                 The margin to the left of the image (default is 0).
        :param margin_right:                The margin to the right of the image (default is 0).
        :param margin_top:                  The margin above the image (default is 0).
        :param padding_bottom:              The padding below the image (default is 0).
        :param padding_left:                The padding to the left of the image (default is 0).
        :param padding_right:               The padding to the right of the image (default is 0).
        :param padding_top:                 The padding above the image (default is 0).
        :param size:                        A tuple defining the width and height of the image (optional).
                                            If not provided, the image will maintain its original dimensions.
        :param vertical_alignment:          The vertical alignment of the image (default is top-aligned).
        """
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
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
        )
        self.__image_source = bytes_path_pil_image_or_url
        self.__image: typing.Optional["PIL.Image.Image"] = None  # type: ignore[name-defined]
        self.__size: typing.Optional[typing.Tuple[int, int]] = size

    #
    # PRIVATE
    #

    def __get_image(self) -> None:

        # IF the image has already been loaded
        # THEN return
        if self.__image is not None:
            return

        # PILImageModule.Image
        try:
            import PIL.Image  # type: ignore[import-untyped, import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'Pillow' library to use the Image class. "
                "You can install it with 'pip install Pillow'."
            )
        if isinstance(self.__image_source, PIL.Image.Image):
            self.__image = self.__image_source

        # URL (str)
        if isinstance(self.__image_source, str):
            try:
                import requests  # type: ignore[import-untyped]
            except ImportError:
                raise ImportError(
                    "Please install the 'requests' library to use the Image class. "
                    "You can install it with 'pip install requests'."
                )
            response = requests.get(
                self.__image_source,
                stream=True,
                headers={"Accept-Encoding": ""},
            )
            bytes_io_source = io.BytesIO(response.content)
            bytes_io_source.seek(0)
            self.__image = PIL.Image.open(bytes_io_source)

        # pathlib.Path
        if isinstance(self.__image_source, pathlib.Path):
            self.__image = PIL.Image.open(self.__image_source)

        # bytes
        if isinstance(self.__image_source, bytes):
            self.__image = PIL.Image.open(io.BytesIO(self.__image_source))

        assert self.__image is not None
        if self.__size is None:
            self.__size = (self.__image.width, self.__image.height)

    def __get_image_bytes(self) -> bytes:

        # force load the image
        self.__get_image()

        # IF the image contains transparency
        # THEN convert to RGBA
        assert self.__image is not None
        if self.__image.has_transparency_data:
            self.__image = self.__image.convert("RGBA")

            # get pixel level information and build byte-array
            s0: typing.List[typing.Tuple[int, int, int]] = [
                (pixel[0], pixel[1], pixel[2]) for pixel in self.__image.getdata()
            ]

            # flatten
            import itertools

            s1: typing.List[int] = [x for x in itertools.chain(*s0)]

            # compress and return
            import zlib

            return zlib.compress(bytes(s1))

        # default
        bytestream = io.BytesIO()
        assert self.__image is not None
        self.__image = self.__image.convert("RGB")
        self.__image.save(bytestream, format="JPEG")
        return bytestream.getvalue()

    def __get_smask_stream(self) -> stream:

        # get raw <alpha> bytes
        assert self.__image is not None
        smask_bytes: bytes = bytes([a for r, g, b, a in self.__image.getdata()])

        # compression
        import zlib

        smask_compressed_bytes = zlib.compress(smask_bytes)

        # construct output value
        out: stream = stream()
        out[name("BitsPerComponent")] = 8
        out[name("Bytes")] = smask_compressed_bytes
        out[name("ColorSpace")] = name("DeviceGray")
        out[name("Filter")] = name("FlateDecode")
        out[name("Height")] = self.__image.width
        out[name("Length")] = len(smask_compressed_bytes)
        out[name("Subtype")] = name("Image")
        out[name("Type")] = name("XObject")
        out[name("Width")] = self.__image.height

        # return
        return out

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
        self.__get_image()
        assert self.__size is not None
        return (
            self.__size[0] + self.get_padding_left() + self.get_padding_right(),
            self.__size[1] + self.get_padding_top() + self.get_padding_bottom(),
        )

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
        # resources
        if "Resources" not in page:
            page["Resources"] = {}
        if "XObject" not in page["Resources"]:
            page["Resources"]["XObject"] = {}

        # create new image_name
        image_name: str = "Im1"
        while image_name in page["Resources"]["XObject"]:
            image_name = f"Im{int(image_name[2:])+1}"
        page["Resources"]["XObject"][image_name] = self.__image

        # Im (stream)
        self.__get_image()
        assert self.__image is not None
        image_stream: stream = stream()
        image_stream["Filter"] = (
            name("FlateDecode")
            if self.__image.has_transparency_data
            else name("DCTDecode")
        )
        image_stream["Bytes"] = self.__get_image_bytes()
        image_stream["Type"] = name("XObject")
        image_stream["Subtype"] = name("Image")
        image_stream["Length"] = len(image_stream["Bytes"])
        image_stream["Width"] = self.__image.width
        image_stream["Height"] = self.__image.height
        image_stream["BitsPerComponent"] = 8
        image_stream["ColorSpace"] = name("DeviceRGB")

        # IF the image is an RGBA image
        # THEN add an SMASK
        if self.__image.mode == "RGBA":
            image_stream[name("SMask")] = self.__get_smask_stream()

        # add Image to Page/Resources/XObject/Im1
        page["Resources"]["XObject"][image_name] = image_stream

        # calculate width and height
        assert self.__size is not None
        w: int = self.__size[0] + self.get_padding_left() + self.get_padding_right()
        h: int = self.__size[1] + self.get_padding_top() + self.get_padding_bottom()

        # calculate where the background/borders need to be painted
        # fmt: off
        background_x: int = available_space[0]
        if self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.LEFT:
            background_x = available_space[0]
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.MIDDLE:
            background_x = available_space[0] + (available_space[2] - w) // 2
        elif self.get_horizontal_alignment() == LayoutElement.HorizontalAlignment.RIGHT:
            background_x = available_space[0] + (available_space[2] - w)
        # fmt: on

        background_y: int = available_space[1]
        if self.get_vertical_alignment() == LayoutElement.VerticalAlignment.BOTTOM:
            background_y = available_space[1]
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.MIDDLE:
            background_y = available_space[1] + (available_space[3] - h) // 2
        elif self.get_vertical_alignment() == LayoutElement.VerticalAlignment.TOP:
            background_y = available_space[1] + (available_space[3] - h)

        # BDC
        # fmt: off
        Image._begin_marked_content_with_dictionary(page=page, structure_element_type='Figure')  # type: ignore[attr-defined]
        # fmt: on

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # leading newline (if needed)
        Image._append_newline_to_content_stream(page)

        # store graphics state
        page["Contents"]["DecodedBytes"] += b"q\n"

        # write cm operator
        page["Contents"]["DecodedBytes"] += (
            f"{self.__size[0]} 0 "
            f"0 {self.__size[1]} "
            f"{background_x + self.get_padding_left()} {background_y + self.get_padding_bottom()} cm\n"
        ).encode("latin1")

        # write Do operator
        page["Contents"]["DecodedBytes"] += f"/{image_name} Do\n".encode("latin1")

        # restore graphics state
        page["Contents"]["DecodedBytes"] += b"Q\n"

        # EMC
        Image._end_marked_content(page=page)  # type: ignore[attr-defined]
