import typing
from decimal import Decimal

from borb.pdf import HexColor, Color, Page
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.layout_element import LayoutElement, Alignment


class ProgressBar(LayoutElement):
    """
    This implementation of LayoutElement represents a basic (no-text) progressbar.
    It displays a rectangular shape of fill_color, overlaid with a (smaller) rectangular shape of
    stroke_color. This implementation of ProgressBar is roughly size 12 font wide.
    """

    def __init__(
        self,
        percentage: float = 0.0,
        vertical_alignment: Alignment = Alignment.TOP,
        horizontal_alignment: Alignment = Alignment.LEFT,
        border_top: bool = False,
        border_right: bool = False,
        border_bottom: bool = False,
        border_left: bool = False,
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_bottom_left: Decimal = Decimal(0),
        border_color: Color = HexColor("000000"),
        border_width: Decimal = Decimal(1),
        padding_top: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        margin_top: typing.Optional[Decimal] = None,
        margin_right: typing.Optional[Decimal] = None,
        margin_bottom: typing.Optional[Decimal] = None,
        margin_left: typing.Optional[Decimal] = None,
        background_color: typing.Optional[Color] = None,
        stroke_color: Color = HexColor("2c99f9"),
        fill_color: Color = HexColor("f0f0f0"),
    ):
        super().__init__(
            font_size=Decimal(0),
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_bottom_left=border_radius_bottom_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            margin_top=margin_top or Decimal(0),
            margin_right=margin_right or Decimal(0),
            margin_bottom=margin_bottom or Decimal(0),
            margin_left=margin_left or Decimal(0),
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
            background_color=background_color,
        )
        assert 0 <= percentage <= 1, "ProgressBar displays percentages between 0 and 1"
        self._percentage: float = percentage
        self._stroke_color: Color = stroke_color
        self._fill_color: Color = fill_color

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:

        # determine height
        h: Decimal = min(bounding_box.get_height(), Decimal(12 * 1.2))
        bb: Rectangle = Rectangle(bounding_box.get_x(),
                                  bounding_box.get_y() + bounding_box.get_height() - h,
                                  bounding_box.get_width(),
                                  h)

        # draw rectangle background
        fill_rgb = (self._fill_color or HexColor("f0f0f0")).to_rgb()
        content = " q %f %f %f RG %f %f %f rg" % (
            Decimal(fill_rgb.red),
            Decimal(fill_rgb.green),
            Decimal(fill_rgb.blue),
            Decimal(fill_rgb.red),
            Decimal(fill_rgb.green),
            Decimal(fill_rgb.blue),
        )
        content += " %f %f %f %f re B" % (bb.get_x(),
                                        bb.get_y(),
                                        bb.get_width(),
                                        bb.get_height())

        # draw active color background
        if self._percentage != 0:
            stroke_rgb = (self._stroke_color or HexColor("2c99f9")).to_rgb()
            content += " %f %f %f RG  %f %f %f rg" % (
                Decimal(stroke_rgb.red),
                Decimal(stroke_rgb.green),
                Decimal(stroke_rgb.blue),
                Decimal(stroke_rgb.red),
                Decimal(stroke_rgb.green),
                Decimal(stroke_rgb.blue),
            )
            content += " %f %f %f %f re B" % (bb.get_x(),
                                        bb.get_y(),
                                        bb.get_width() * Decimal(self._percentage),
                                        bb.get_height())

        # end stack
        content += " Q"

        # append to page
        self._append_to_content_stream(page, content)

        # set bounding box
        self.set_bounding_box(bb)

        # return
        return bb


class ProgressSquare(ProgressBar):
    """
    This implementation of LayoutElement represents a basic (no-text) progressbar.
    It displays a rectangular shape of fill_color, overlaid with a (smaller) rectangular shape of
    stroke_color. This implementation of ProgressBar is roughly size 12 font tall AND wide.
    """

    def _do_layout_without_padding(
        self, page: Page, bounding_box: Rectangle
    ) -> Rectangle:
        h: Decimal = min(bounding_box.get_height(), Decimal(12 * 1.2))
        return super(ProgressSquare, self)._do_layout_without_padding(page,
                                                                      Rectangle(bounding_box.get_x(),
                                                                                bounding_box.get_y() + bounding_box.get_height() - h,
                                                                                h,
                                                                                h))