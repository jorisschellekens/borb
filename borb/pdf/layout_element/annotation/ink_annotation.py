#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Represents an ink annotation in a PDF document.

An ink annotation (PDF 1.3) represents a freehand “scribble” composed of one or more
disjoint paths. When opened, it displays a pop-up window containing the text of the
associated note.

Table 182 shows the annotation dictionary entries specific to this type of annotation.
"""


import math
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.x11_color import X11Color
from borb.pdf.layout_element.annotation.annotation import Annotation
from borb.pdf.layout_element.layout_element import LayoutElement
from borb.pdf.layout_element.shape.shape import Shape
from borb.pdf.page import Page
from borb.pdf.primitives import name


class InkAnnotation(Annotation):
    """
    Represents an ink annotation in a PDF document.

    An ink annotation (PDF 1.3) represents a freehand “scribble” composed of one or more
    disjoint paths. When opened, it displays a pop-up window containing the text of the
    associated note.

    Table 182 shows the annotation dictionary entries specific to this type of annotation.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        shape: Shape,
        background_color: typing.Optional[Color] = None,
        border_color: typing.Optional[Color] = None,
        border_dash_pattern: typing.List[int] = [],
        border_dash_phase: int = 0,
        border_width_bottom: int = 0,
        border_width_left: int = 0,
        border_width_right: int = 0,
        border_width_top: int = 0,
        contents: typing.Optional[str] = None,
        horizontal_alignment: LayoutElement.HorizontalAlignment = LayoutElement.HorizontalAlignment.LEFT,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        padding_bottom: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        size: typing.Tuple[int, int] = (100, 00),
        stroke_color: typing.Optional[Color] = X11Color.BLACK,
        vertical_alignment: LayoutElement.VerticalAlignment = LayoutElement.VerticalAlignment.TOP,
    ):
        """
        Initialize a new `InkAnnotation` object for rendering freehand ink annotations in a PDF.

        This constructor allows customization of various layout and style properties
        for the ink annotation, such as shape, background color, borders, size, contents,
        and alignment. These properties define the appearance and positioning of the ink
        annotation within the PDF page.

        :param shape:                    The `Shape` object that defines the ink strokes of the annotation.
        :param background_color:         Optional background color for the ink annotation container.
        :param border_color:             Optional border color for the annotation container.
        :param border_dash_pattern:      Dash pattern used for the annotation border lines.
        :param border_dash_phase:        Phase offset for the dash pattern in the annotation borders.
        :param border_width_bottom:      Width of the bottom border of the annotation container.
        :param border_width_left:        Width of the left border of the annotation container.
        :param border_width_right:       Width of the right border of the annotation container.
        :param border_width_top:         Width of the top border of the annotation container.
        :param contents:                 Optional text content for the annotation.
        :param horizontal_alignment:     Horizontal alignment of the annotation (default is LEFT).
        :param padding_bottom:           Padding inside the annotation container at the bottom.
        :param padding_left:             Padding inside the annotation container on the left side.
        :param padding_right:            Padding inside the annotation container on the right side.
        :param padding_top:              Padding inside the annotation container at the top.
        :param size:                     Tuple representing the width and height of the annotation.
        :param stroke_color:             Color of the ink strokes (default is BLACK).
        :param vertical_alignment:       Vertical alignment of the annotation (default is TOP).
        """
        self.__shape: Shape = shape.scale_to_fit(size=size)
        super().__init__(
            background_color=background_color,
            border_color=border_color,
            border_dash_pattern=border_dash_pattern,
            border_dash_phase=border_dash_phase,
            border_width_bottom=border_width_bottom,
            border_width_left=border_width_left,
            border_width_right=border_width_right,
            border_width_top=border_width_top,
            contents=contents,
            fill_color=None,
            horizontal_alignment=horizontal_alignment,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_left=padding_left,
            padding_bottom=padding_bottom,
            size=size,
            stroke_color=stroke_color,
            vertical_alignment=vertical_alignment,
        )

        # (Required) The type of annotation that this dictionary describes; shall be
        # Ink for an ink annotation.
        self["Subtype"] = name("Ink")

    #
    # PRIVATE
    #

    @staticmethod
    def __flatten_and_move_polygon(
        polygon: typing.List[typing.Tuple[float, float]], x_delta: float, y_delta: float
    ) -> typing.List[float]:
        m: typing.List[float] = []
        for x, y in polygon:
            m.append(x + x_delta)
            m.append(y + y_delta)
        return m

    #
    # PUBLIC
    #

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
        super().paint(available_space=available_space, page=page)

        # determine paint coordinates
        x, y, _, _ = self["Rect"]

        # determine min_x, min_y (so that we can move the Shape object in the right direction afterwards)
        min_x: float = math.inf
        min_y: float = math.inf
        if isinstance(self.__shape.get_polygons()[0], list):
            # fmt: off
            min_x = min([min([x for x, _ in polygon]) for polygon in self.__shape.get_polygons()])   # type: ignore[misc]
            min_y = min([min([y for _, y in polygon]) for polygon in self.__shape.get_polygons()])   # type: ignore[misc]
            # fmt: on
        else:
            min_x = min([x for x, _ in self.__shape.get_polygons()])  # type: ignore[assignment]
            min_y = min([y for _, y in self.__shape.get_polygons()])  # type: ignore[assignment]

        # (Required) An array of n arrays, each representing a stroked path. Each
        # array shall be a series of alternating horizontal and vertical coordinates in
        # default user space, specifying points along the path. When drawn, the
        # points shall be connected by straight lines or curves in an
        # implementation-dependent way.
        if isinstance(self.__shape.get_polygons()[0], list):
            self["InkList"] = [
                InkAnnotation.__flatten_and_move_polygon(
                    polygon=polygon, x_delta=x - min_x, y_delta=y - min_y  # type: ignore[arg-type]
                )
                for polygon in self.__shape.get_polygons()
            ]
        else:
            self["InkList"] = [
                InkAnnotation.__flatten_and_move_polygon(
                    polygon=self.__shape.get_polygons(),  # type: ignore[arg-type]
                    x_delta=x - min_x,
                    y_delta=y - min_y,
                )
            ]
