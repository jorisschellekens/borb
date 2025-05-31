#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an AI-generated image that can be inserted into a PDF document.

The DallE class inherits from the Image class in the PDF library, allowing users to insert
AI-generated images directly into PDF documents. Users provide a prompt, which is sent to
the DALL·E API, and the generated image is retrieved and embedded in the PDF.
"""
import os
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class DallE(Image):
    """
    Represents an AI-generated image that can be inserted into a PDF document.

    The DallE class inherits from the Image class in the PDF library, allowing users to insert
    AI-generated images directly into PDF documents. Users provide a prompt, which is sent to
    the DALL·E API, and the generated image is retrieved and embedded in the PDF.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        prompt: str,
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
        Initialize the DAllE object representing an image generated from a user-specified prompt.

        The `DAllE` class allows users to generate images based on textual descriptions using OpenAI's DALL·E model.
        This constructor initializes the attributes required for the image generation process,
        including the prompt, optional background and border colors, layout options, and size specifications.
        These attributes influence how the image is rendered and displayed within the application.

        :param prompt:                  The textual description that will be sent to DALL·E to generate the image.
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
            bytes_path_pil_image_or_url=DallE.__get_image(
                prompt=prompt,
                size=size or (512, 512),
            ),
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
            size=size,
            vertical_alignment=vertical_alignment,
        )

    #
    # PRIVATE
    #

    @staticmethod
    def __get_image(prompt: str, size: typing.Tuple[int, int]) -> str:

        # send a request to OpenAI
        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'openai' library to use the DallE class. "
                "You can install it with 'pip install openai'."
            )

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        r: float = size[0] / size[1]
        if abs(r - 0.57) <= abs(r - 1) and abs(r - 0.57) <= abs(r - 1.75):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1792",
                quality="standard",
                n=1,
            )
        elif abs(r - 1) <= abs(r - 0.57) and abs(r - 1) <= abs(r - 1.75):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
        elif abs(r - 1.75) <= abs(r - 0.57) and abs(r - 1.75) <= abs(r - 1):
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",
                quality="standard",
                n=1,
            )
        else:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

        # Get the image_tests URL from the response
        assert response.data[0].url is not None
        return response.data[0].url

    #
    # PUBLIC
    #
