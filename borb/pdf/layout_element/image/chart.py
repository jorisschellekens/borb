#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a chart generated using Matplotlib for insertion into a PDF document.

The Chart class allows users to embed Matplotlib plots as LayoutElement objects in PDF
documents. It inherits from the Image class, enabling the conversion of Matplotlib figures
into images that can be placed within the layout of the PDF.
"""
import io
import typing

from borb.pdf.color.color import Color
from borb.pdf.layout_element.image.image import Image
from borb.pdf.layout_element.layout_element import LayoutElement


class Chart(Image):
    """
    Represents a chart generated using Matplotlib for insertion into a PDF document.

    The Chart class allows users to embed Matplotlib plots as LayoutElement objects in PDF
    documents. It inherits from the Image class, enabling the conversion of Matplotlib figures
    into images that can be placed within the layout of the PDF.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        matplotlib_plt: "matplotlib.pyplot",  # type: ignore[name-defined]
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
        Initialize the Chart object to wrap around a matplotlib plot with specified attributes.

        The `Chart` class serves as a wrapper around the matplotlib plotting library,
        enabling users to create and customize plots easily.
        This constructor initializes the chart with various attributes,
        including the underlying matplotlib plotting object, optional styling elements
        such as background and border colors, layout settings, and size specifications.
        These attributes dictate how the chart is rendered and displayed,
        providing flexibility for different visual presentations.

        :param matplotlib_plt:          The matplotlib plotting module used to create the chart. This should be an instance of matplotlib.pyplot.
        :param background_color:        Optional color for the chart background. Default is None.
        :param border_color:            Optional color for the border around the chart. Default is None.
        :param border_dash_pattern:     A list defining the dash pattern for the border. Default is an empty list.
        :param border_dash_phase:       The phase offset for the dash pattern. Default is 0.
        :param border_width_bottom:     Width of the border at the bottom of the chart. Default is 0.
        :param border_width_left:       Width of the border on the left side of the chart. Default is 0.
        :param border_width_right:      Width of the border on the right side of the chart. Default is 0.
        :param border_width_top:        Width of the border at the top of the chart. Default is 0.
        :param horizontal_alignment:    Alignment of the chart horizontally within its layout. Default is LayoutElement.HorizontalAlignment.LEFT.
        :param margin_bottom:           Bottom margin for spacing around the chart. Default is 0.
        :param margin_left:             Left margin for spacing around the chart. Default is 0.
        :param margin_right:            Right margin for spacing around the chart. Default is 0.
        :param margin_top:              Top margin for spacing around the chart. Default is 0.
        :param padding_bottom:          Padding at the bottom of the chart. Default is 0.
        :param padding_left:            Padding on the left side of the chart. Default is 0.
        :param padding_right:           Padding on the right side of the chart. Default is 0.
        :param padding_top:             Padding at the top of the chart. Default is 0.
        :param size:                    Optional tuple specifying the dimensions of the chart as (width, height). Default is None.
        :param vertical_alignment:      Alignment of the chart vertically within its layout. Default is LayoutElement.VerticalAlignment.TOP.
        """
        super().__init__(
            bytes_path_pil_image_or_url=Chart.__get_image(
                matplotlib_plt=matplotlib_plt
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
    def __get_image(matplotlib_plt: "matplotlib.pyplot") -> bytes:  # type: ignore[name-defined]

        # try setting the dpi
        try:
            matplotlib_plt.dpi = max(600, matplotlib_plt.dpi)
        except:
            pass

        # chart to image
        byte_buffer = io.BytesIO()
        matplotlib_plt.savefig(byte_buffer, format="png")
        byte_buffer.seek(0)

        # return bytes
        return byte_buffer.getvalue()

    #
    # PUBLIC
    #
