import typing
from typing import Tuple

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import Color
from ptext.pdf.canvas.geometry.rectangle import Rectangle
from ptext.pdf.canvas.layout.paragraph import LayoutElement
from ptext.pdf.page.page import Page


class Shape(LayoutElement):
    """
    This class represents a generic shape (specified by a List of points).
    It has convenience methods to calculate width and height, perform scaling, etc
    """

    def __init__(
        self,
        points: typing.List[Tuple[Decimal, Decimal]],
        stroke_color: typing.Optional[Color],
        fill_color: typing.Optional[Color],
        line_width: typing.Optional[Decimal],
        preserve_aspect_ratio: bool = True,
    ):
        assert len(points) >= 3
        self.points = points
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.line_width = line_width
        self.preserve_aspect_ratio = preserve_aspect_ratio

    def get_width(self) -> Decimal:
        """
        This function returns the width of this Shape
        """
        min_x = min([x[0] for x in self.points])
        max_x = max([x[0] for x in self.points])
        return max_x - min_x

    def get_height(self) -> Decimal:
        """
        This function returns the height of this Shape
        """
        min_y = min([x[1] for x in self.points])
        max_y = max([x[1] for x in self.points])
        return max_y - min_y

    def scale_to_fit(self, max_width: Decimal, max_height: Decimal) -> "Shape":
        """
        This method scales this Shape to fit a given max. width / height
        """
        w_scale = max_width / self.get_width()
        h_scale = max_height / self.get_height()
        if self.preserve_aspect_ratio:
            w_scale = min(w_scale, h_scale)
            h_scale = w_scale
        if w_scale < 1:
            self.points = [(x[0] * w_scale, x[1]) for x in self.points]
        if h_scale < 1:
            self.points = [(x[0], x[1] * h_scale) for x in self.points]
        return self

    def translate_to_align(self, lower_left_x: Decimal, lower_left_y: Decimal):
        min_x = min([x[0] for x in self.points])
        min_y = min([x[1] for x in self.points])
        delta_x = lower_left_x - min_x
        delta_y = lower_left_y - min_y
        self.points = [(x[0] + delta_x, x[1] + delta_y) for x in self.points]

    def layout(self, page: Page, bounding_box: Rectangle) -> Rectangle:

        # scale to fit
        self.scale_to_fit(bounding_box.width, bounding_box.height)

        # translate points to fit in box
        self.translate_to_align(
            bounding_box.x, bounding_box.y + bounding_box.height - self.get_height()
        )

        # write content
        stroke_rgb = self.stroke_color.to_rgb()
        fill_rgb = self.fill_color.to_rgb()
        COLOR_MAX = Decimal(255.0)
        content = "q %f %f %f RG  % f %f %f rg %f w " % (
            Decimal(stroke_rgb.red / COLOR_MAX),
            Decimal(stroke_rgb.green / COLOR_MAX),
            Decimal(stroke_rgb.blue / COLOR_MAX),
            Decimal(fill_rgb.red / COLOR_MAX),
            Decimal(fill_rgb.green / COLOR_MAX),
            Decimal(fill_rgb.blue / COLOR_MAX),
            self.line_width,
        )
        content += "%f %f m " % (self.points[0][0], self.points[0][1])
        for p in self.points:
            content += " %f %f l " % (p[0], p[1])
        content += " B Q"

        # append to page
        self._append_to_content_stream(page, content)

        # calculate bounding box
        layout_rect = Rectangle(
            bounding_box.x,
            bounding_box.y + bounding_box.height - self.get_height(),
            self.get_width(),
            self.get_height(),
        )

        # set bounding box
        self.set_bounding_box(layout_rect)

        # return
        return layout_rect
