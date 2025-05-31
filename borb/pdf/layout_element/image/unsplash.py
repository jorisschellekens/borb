#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an image retrieved from the Unsplash API, which can be inserted into a PDF document.

The `Unsplash` class allows users to provide search keywords to find a relevant image from the
Unsplash image database. This class interacts with the Unsplash API, retrieves the image, and
embeds it into a PDF document, inheriting functionality from the `Image` class.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class Unsplash(Image):
    """
    Represents an Image retrieved from the Unsplash API, which can be inserted into a PDF document.

    The `Unsplash` class allows users to provide search keywords to find a relevant image from the
    Unsplash image database. This class interacts with the Unsplash API, retrieves the image, and
    embeds it into a PDF document, inheriting functionality from the `Image` class.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        keywords: typing.List[str],
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
        Initialize the UnsplashAPI object to retrieve images based on specified keywords.

        The `UnsplashAPI` class interacts with the Unsplash API to fetch images that match the given keywords.
        This constructor sets up the necessary attributes for image retrieval and display, including the keywords,
        optional background and border colors, layout settings, and image dimensions.
        These attributes determine how the images are displayed in the application
        and allow for customization of the visual presentation.

        :param keywords:                A list of keywords used to search for relevant images from the Unsplash API.
        :param background_color:        Optional color for the background of the image. Default is None.
        :param border_color:            Optional color for the border surrounding the image. Default is None.
        :param border_dash_pattern:     A list defining the dash pattern for the border. Default is an empty list.
        :param border_dash_phase:       The phase offset for the dash pattern. Default is 0.
        :param border_width_bottom:     Width of the border at the bottom of the image. Default is 0.
        :param border_width_left:       Width of the border on the left side of the image. Default is 0.
        :param border_width_right:      Width of the border on the right side of the image. Default is 0.
        :param border_width_top:        Width of the border at the top of the image. Default is 0.
        :param horizontal_alignment:    Alignment of the image horizontally within its layout. Default is LayoutElement.HorizontalAlignment.LEFT.
        :param margin_bottom:           Bottom margin for spacing around the image. Default is 0.
        :param margin_left:             Left margin for spacing around the image. Default is 0.
        :param margin_right:            Right margin for spacing around the image. Default is 0.
        :param margin_top:              Top margin for spacing around the image. Default is 0.
        :param padding_bottom:          Padding at the bottom of the image. Default is 0.
        :param padding_left:            Padding on the left side of the image. Default is 0.
        :param padding_right:           Padding on the right side of the image. Default is 0.
        :param padding_top:             Padding at the top of the image. Default is 0.
        :param size:                    Optional tuple specifying the dimensions of the image as (width, height). Default is None.
        :param vertical_alignment:      Alignment of the image vertically within its layout. Default is LayoutElement.VerticalAlignment.TOP.
        """
        super().__init__(
            bytes_path_pil_image_or_url=Unsplash.__get_image(
                keywords=keywords,
                size=size,
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
        keywords: typing.List[str],
        size: typing.Optional[typing.Tuple[int, int]] = None,
    ) -> str:

        # calculate desired aspect ratio
        desired_aspect_ratio: typing.Optional[float] = None
        if size is not None:
            desired_aspect_ratio = size[0] / size[1]

        # build keyword str
        keyword_str: str = "".join([(k + "+") for k in keywords])[:-1]

        # get UNSPLASH_API_KEY
        # fmt: off
        import os
        unsplash_access_key: typing.Optional[str] = os.environ.get("UNSPLASH_API_KEY")
        assert unsplash_access_key is not None, "UNSPLASH_API_KEY not found in os.environ"
        # fmt: on

        # fetch json
        import json
        import urllib.request

        url: str = (
            "https://api.unsplash.com/search/photos?page=1&query=%s&client_id=%s"
            % (keyword_str, unsplash_access_key)
        )
        min_aspect_ratio_delta: typing.Optional[float] = None
        min_image: typing.Optional[str] = None
        with urllib.request.urlopen(url) as response:
            for result in json.loads(response.read().decode())["results"]:
                if "width" not in result:
                    continue
                if "height" not in result:
                    continue
                if "urls" not in result:
                    continue
                if "regular" not in result["urls"]:
                    continue
                w: float = float(result["width"])
                h: float = float(result["height"])
                r: float = w / h
                if desired_aspect_ratio is not None:
                    aspect_ratio_delta: float = abs(r - desired_aspect_ratio)
                    if (
                        min_aspect_ratio_delta is None
                        or aspect_ratio_delta < min_aspect_ratio_delta
                    ):
                        min_aspect_ratio_delta = aspect_ratio_delta
                        min_image = result["urls"]["regular"]
                else:
                    if min_image is None:
                        min_image = result["urls"]["regular"]

        # return
        assert min_image is not None
        return min_image

    #
    # PUBLIC
    #
