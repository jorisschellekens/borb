#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A class that uses matplotlib and LaTeX to render mathematical equations as images.

The `Equation` class extends the `Image` class and provides functionality to
generate a high-quality image of a mathematical equation. It utilizes LaTeX for
typesetting the equation and matplotlib for rendering the LaTeX code as an image.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class Equation(Image):
    """
    A class that uses matplotlib and LaTeX to render mathematical equations as images.

    The `Equation` class extends the `Image` class and provides functionality to
    generate a high-quality image of a mathematical equation. It utilizes LaTeX for
    typesetting the equation and matplotlib for rendering the LaTeX code as an image.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        latex_syntax: str,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        font_color: Color = X11Color.BLACK,
        font_size: int = 12,
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
        Initialize an Equation object to render a LaTeX mathematical equation as an image.

        The `Equation` class uses LaTeX syntax to render mathematical equations into an image.
        The image can be customized with various layout properties such as background color, borders, padding, margins, font styles, and alignment.

        :param latex_syntax:            A LaTeX string representing the mathematical equation to render.
        :param background_color:        Optional color for the background of the image. Default is None.
        :param border_color:            Optional color for the border surrounding the image. Default is None.
        :param border_dash_pattern:     A list defining the dash pattern for the border. Default is an empty list (solid border).
        :param border_dash_phase:       The phase offset for the dash pattern. Default is 0.
        :param border_width_bottom:     Width of the border at the bottom of the image. Default is 0 (no border).
        :param border_width_left:       Width of the border on the left side of the image. Default is 0 (no border).
        :param border_width_right:      Width of the border on the right side of the image. Default is 0 (no border).
        :param border_width_top:        Width of the border at the top of the image. Default is 0 (no border).
        :param font_color:              Color of the text (equation). Default is black (X11Color.BLACK).
        :param font_size:               Size of the font used to render the equation. Default is 12.
        :param horizontal_alignment:    Horizontal alignment of the equation within the image. Default is `LEFT`.
        :param margin_bottom:           Bottom margin for spacing around the image. Default is 0.
        :param margin_left:             Left margin for spacing around the image. Default is 0.
        :param margin_right:            Right margin for spacing around the image. Default is 0.
        :param margin_top:              Top margin for spacing around the image. Default is 0.
        :param padding_bottom:          Padding at the bottom of the image. Default is 0.
        :param padding_left:            Padding on the left side of the image. Default is 0.
        :param padding_right:           Padding on the right side of the image. Default is 0.
        :param padding_top:             Padding at the top of the image. Default is 0.
        :param size:                    Optional tuple specifying the dimensions of the image as (width, height). Default is None, which automatically adjusts the size based on content.
        :param vertical_alignment:      Vertical alignment of the equation within the image. Default is `TOP`.
        """
        super().__init__(
            bytes_path_pil_image_or_url=Equation.__get_image(
                latex_syntax=latex_syntax,
                font_size=int((font_size - 2.5) / 7.7),
                font_color=font_color,
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
        latex_syntax: str,
        background_color: Color = X11Color.WHITE,
        dpi: int = 600,
        font_color: Color = X11Color.BLACK,
        font_size: int = 12,
        format: str = "JPEG",
    ) -> bytes:
        import io

        try:
            import matplotlib.pyplot  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "Please install the 'matplotlib' library to use the __get_image method in the Equation class. "
                "You can install it with 'pip install matplotlib'."
            )
        font_color_as_rgb: RGBColor = font_color.to_rgb_color()
        r0, g0, b0 = (
            font_color_as_rgb.get_red(),
            font_color_as_rgb.get_green(),
            font_color_as_rgb.get_blue(),
        )
        fig = matplotlib.pyplot.figure(figsize=(1, 1))
        fig.text(
            x=0,
            y=0,
            s="${}$".format(latex_syntax),
            fontsize=font_size,
            color=(r0 / 255, g0 / 255, b0 / 255),
        )

        # store
        background_color_as_rgb: RGBColor = background_color.to_rgb_color()
        r1, g1, b1 = (
            background_color_as_rgb.get_red(),
            background_color_as_rgb.get_green(),
            background_color_as_rgb.get_blue(),
        )
        buffer_ = io.BytesIO()
        fig.savefig(
            buffer_,
            dpi=dpi,
            facecolor=(r1 / 255, g1 / 255, b1 / 255),
            format=format,
            bbox_inches="tight",
            pad_inches=0.0,
        )
        matplotlib.pyplot.close(fig)
        return buffer_.getvalue()

    #
    # PUBLIC
    #
