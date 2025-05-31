#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents a PDF annotation, which supports various standard annotation types.

PDF supports several standard annotation types, as listed in Table 169. This class describes
these types and their functionalities in detail. The values in the first column of Table 169
correspond to the annotation dictionary's Subtype entry. Additionally, the third column indicates
whether the annotation is a markup annotation, as detailed in Section 12.5.6.2, “Markup Annotations.”
This class also provides information about the value of the Contents entry for different annotation types.
"""
import functools
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.page import Page
from borb.pdf.primitives import name


class Annotation(LayoutElement, dict):
    """
    Represents a PDF annotation, which supports various standard annotation types.

    PDF supports several standard annotation types, as listed in Table 169. This class describes
    these types and their functionalities in detail. The values in the first column of Table 169
    correspond to the annotation dictionary's Subtype entry. Additionally, the third column indicates
    whether the annotation is a markup annotation, as detailed in Section 12.5.6.2, “Markup Annotations.”
    This class also provides information about the value of the Contents entry for different annotation types.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        contents: typing.Optional[str] = None,
        fill_color: typing.Optional[Color] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: typing.Tuple[int, int] = (100, 100),
        stroke_color: typing.Optional[Color] = None,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new `Annotation` object for rendering annotations in a PDF document.

        This constructor allows customization of various properties related to the
        annotation's appearance and layout, including background color, border styles,
        padding, size, contents, and alignment. These properties are essential for
        defining how the annotation will be presented within the PDF.

        :param background_color:         Optional background color for the annotation.
        :param border_color:             Optional border color for the annotation.
        :param border_dash_pattern:      Dash pattern used for the annotation's border lines.
        :param border_dash_phase:        Phase offset for the dash pattern in the annotation borders.
        :param border_width_bottom:      Width of the bottom border of the annotation.
        :param border_width_left:        Width of the left border of the annotation.
        :param border_width_right:       Width of the right border of the annotation.
        :param border_width_top:         Width of the top border of the annotation.
        :param contents:                 Optional text content for the annotation.
        :param fill_color:               Optional fill color for the annotation.
        :param horizontal_alignment:      Horizontal alignment of the annotation (default is LEFT).
        :param margin_bottom:           Space between the annotation and the element below it.
        :param margin_left:             Space between the annotation and the left page margin.
        :param margin_right:            Space between the annotation and the right page margin.
        :param margin_top:              Space between the annotation and the element above it.
        :param padding_bottom:           Padding inside the annotation at the bottom.
        :param padding_left:             Padding inside the annotation on the left side.
        :param padding_right:            Padding inside the annotation on the right side.
        :param padding_top:              Padding inside the annotation at the top.
        :param size:                     Tuple representing the width and height of the annotation.
        :param stroke_color:             Optional color for the annotation's stroke (default is None).
        :param vertical_alignment:        Vertical alignment of the annotation (default is TOP).
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
            margin_top=margin_top,
            margin_right=margin_right,
            margin_left=margin_left,
            margin_bottom=margin_bottom,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            vertical_alignment=vertical_alignment,
        )

        # (Optional) The type of PDF object that this dictionary describes; if
        # present, shall be Annot for an annotation dictionary.
        self["Type"] = name("Annot")

        # (Required) The annotation rectangle, defining the location of the
        # annotation on the page in default user space units.
        assert size[0] >= 0 and size[1] >= 0, (
            "The annotation size must have non-negative dimensions. "
            f"Received size: {size}. Ensure width (size[0]) and height (size[1]) are greater than or equal to 0."
        )
        self.__size: typing.Tuple[int, int] = size
        self["Rect"] = [0, 0, self.__size[0], self.__size[1]]

        # (Optional) Text that shall be displayed for the annotation or, if this type of
        # annotation does not display text, an alternate description of the
        # annotation’s contents in human-readable form. In either case, this text is
        # useful when extracting the document’s contents in support of
        # accessibility to users with disabilities or for other purposes (see 14.9.3,
        # “Alternate Descriptions”). See 12.5.6, “Annotation Types” for more
        # details on the meaning of this entry for each annotation type.
        if contents is not None and len(contents) > 0:
            self["Contents"] = contents

        # (Optional; PDF 1.4) The annotation name, a text string uniquely
        # identifying it among all the annotations on its page.
        self["NM"] = ""

        # (Optional; PDF 1.1) The date and time when the annotation was most
        # recently modified. The format should be a date string as described in
        # 7.9.4, “Dates,” but conforming readers shall accept and display a string
        # in any format.
        from datetime import datetime

        self["M"] = datetime.now().strftime("D:%Y%m%d%H%M%S+00'00'")

        # (Optional; PDF 1.1) An array of numbers in the range 0.0 to 1.0,
        # representing a colour used for the following purposes:
        # The background of the annotation’s icon when closed
        # The title bar of the annotation’s pop-up window
        # The border of a link annotation
        # The number of array elements determines the colour space in which the
        # colour shall be defined:
        # 0 No colour; transparent
        # 1 DeviceGray
        # 3 DeviceRGB
        # 4 DeviceCMYK
        if stroke_color is not None:
            rgb_stroke_color: RGBColor = stroke_color.to_rgb_color()
            self["C"] = [
                rgb_stroke_color.get_red() / 255,
                rgb_stroke_color.get_green() / 255,
                rgb_stroke_color.get_blue() / 255,
            ]

        # (Optional; PDF 1.4) An array of numbers that shall be in the range 0.0 to
        # 1.0 and shall specify the interior color with which to fill the annotation’s
        # rectangle or ellipse. The number of array elements determines the colour
        # space in which the colour shall be defined
        if fill_color is not None:
            rgb_fill_color: RGBColor = fill_color.to_rgb_color()
            self["IC"] = [
                rgb_fill_color.get_red() / 255,
                rgb_fill_color.get_green() / 255,
                rgb_fill_color.get_blue() / 255,
            ]

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    @functools.cache
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
        # calculate width and height
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

        # paint background/borders
        super()._paint_background_and_borders(
            page=page, rectangle=(background_x, background_y, w, h)
        )
        self._LayoutElement__previous_paint_box = (background_x, background_y, w, h)

        # (Required) The annotation rectangle, defining the location of the
        # annotation on the page in default user space units.
        self["Rect"] = [
            background_x + self.get_padding_left(),
            background_y + self.get_padding_bottom(),
            background_x + self.get_padding_left() + self.__size[0],
            background_y + self.get_padding_bottom() + self.__size[1],
        ]

        # (Optional; PDF 1.4) The annotation name, a text string uniquely
        # identifying it among all the annotations on its page.
        if "Annots" not in page:
            page["Annots"] = []
        if self not in page["Annots"]:
            self["NM"] = "annotation-{0:03d}".format(len(page["Annots"]))
            page["Annots"] += [self]
