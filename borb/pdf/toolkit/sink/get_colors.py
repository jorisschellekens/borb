#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Sink that processes PDF rendering events to extract and track colors used in a document.

This class listens to events in the PDF processing pipeline and extracts a limited number
of unique colors based on the specified maximum threshold.
"""
import typing

from borb.pdf.color.color import Color
from borb.pdf.color.hsv_color import HSVColor
from borb.pdf.color.rgb_color import RGBColor
from borb.pdf.toolkit.event import Event
from borb.pdf.toolkit.sink.sink import Sink
from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent
from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent
from borb.pdf.toolkit.source.event.text_event import TextEvent


class GetColors(Sink):
    """
    A Sink that processes PDF rendering events to extract and track colors used in a document.

    This class listens to events in the PDF processing pipeline and extracts a limited number
    of unique colors based on the specified maximum threshold.
    """

    #
    # CONSTRUCTOR
    #
    def __init__(self, max_number_of_colors: int = 64):
        """
        Initialize the GetColors sink.

        This constructor sets the maximum number of colors that will be tracked
        when processing a PDF document.

        :param max_number_of_colors: The maximum number of unique colors to track (default: 64).
                                     Must be a positive integer.
        """
        super().__init__()
        assert max_number_of_colors > 0
        self.__max_number_of_colors: int = max_number_of_colors
        self.__number_of_colored_points_per_page: typing.Dict[
            int, typing.Dict[typing.Tuple[int, int, int], int]
        ] = {}

    #
    # PRIVATE
    #

    def __count_shape_fill_event(self, e: ShapeFillEvent) -> None:
        # count area using shoelace theorem
        area: float = 0
        for p0, p1 in e.get_shape():
            x0, y0 = p0
            x1, y1 = p1
            area += x0 * y1 - x1 * y0
        area = abs(area) / 2.0

        # find nearest color
        page_nr: int = e.get_page_nr()
        nearest_color: typing.Tuple[int, int, int] = GetColors.__nearest_color(
            c=e.get_fill_color(),
            cs=self.__number_of_colored_points_per_page[page_nr].keys(),
        )

        # count
        self.__number_of_colored_points_per_page[page_nr][nearest_color] += int(area)

    def __count_shape_stroke_event(self, e: ShapeStrokeEvent) -> None:
        page_nr: int = e.get_page_nr()
        total_length: float = sum(
            [
                ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5
                for (x0, y0), (x1, y1) in e.get_shape()
            ]
        )
        nearest_color: typing.Tuple[int, int, int] = GetColors.__nearest_color(
            c=e.get_stroke_color(),
            cs=self.__number_of_colored_points_per_page[page_nr].keys(),
        )
        self.__number_of_colored_points_per_page[page_nr][nearest_color] += int(
            total_length
        )
        return

    def __count_text_event(self, e: TextEvent) -> None:
        page_nr: int = e.get_page_nr()
        nearest_color: typing.Tuple[int, int, int] = GetColors.__nearest_color(
            c=e.get_font_color(),
            cs=self.__number_of_colored_points_per_page[page_nr].keys(),
        )
        self.__number_of_colored_points_per_page[page_nr][nearest_color] += int(
            e.get_width() * e.get_height()
        )

    @staticmethod
    def __evenly_distributed_colors(n: int) -> typing.List[typing.Tuple[int, int, int]]:
        rgb_colors: typing.List[RGBColor] = [
            HSVColor(hue=angle, saturation=0.5, value=0.5).to_rgb_color()
            for angle in [i * (360 / n) for i in range(n)]
        ]
        return [(c.get_red(), c.get_green(), c.get_blue()) for c in rgb_colors]

    @staticmethod
    def __nearest_color(
        c: Color, cs: typing.Iterable[typing.Tuple[int, int, int]]
    ) -> typing.Tuple[int, int, int]:
        r1: int = c.to_rgb_color().get_red()
        g1: int = c.to_rgb_color().get_green()
        b1: int = c.to_rgb_color().get_blue()
        min_distance: typing.Optional[int] = None
        min_color: typing.Optional[typing.Tuple[int, int, int]] = None
        for r0, g0, b0 in cs:
            d: int = ((r0 - r1) ** 2 + (g0 - g1) ** 2 + (b0 - b1) ** 2) ** 0.5
            if min_distance is None or d < min_distance:
                min_distance = d
                min_color = r0, g0, b0
        assert min_color is not None
        return min_color

    #
    # PUBLIC
    #

    def get_output(self) -> typing.Any:
        """
        Retrieve the aggregated results from the pipeline.

        This method should be overridden by subclasses to provide the specific output
        collected by the `Sink`. By default, it returns `None`, indicating that no
        aggregation or processing has been implemented.

        :return: The aggregated output from the pipeline, or `None` if not implemented.
        """
        return {
            k0: {k1: v1 for k1, v1 in v0.items() if v1 != 0}
            for k0, v0 in self.__number_of_colored_points_per_page.items()
        }

    def process(self, event: Event) -> None:
        """
        Process the given event.

        This base implementation is a no-op. Subclasses should override this method
        to provide specific processing logic.

        :param event: The event object to process.
        """
        page_nr: int = event.get_page_nr()
        if page_nr not in self.__number_of_colored_points_per_page:
            self.__number_of_colored_points_per_page[page_nr] = {
                c: 0
                for c in GetColors.__evenly_distributed_colors(
                    self.__max_number_of_colors
                )
            }

        # ShapeFillEvent
        from borb.pdf.toolkit.source.event.shape_fill_event import ShapeFillEvent

        if isinstance(event, ShapeFillEvent):
            self.__count_shape_fill_event(event)
            return

        # ShapeStrokeEvent
        from borb.pdf.toolkit.source.event.shape_stroke_event import ShapeStrokeEvent

        if isinstance(event, ShapeStrokeEvent):
            self.__count_shape_stroke_event(event)
            return

        # TextEvent
        from borb.pdf.toolkit.source.event.text_event import TextEvent

        if isinstance(event, TextEvent):
            self.__count_text_event(event)
            return

        # ImageEvent
        from borb.pdf.toolkit.source.event.image_event import ImageEvent

        if isinstance(event, ImageEvent):
            w: int = int(event.get_width())
            h: int = int(event.get_height())
            # TODO
            pass
