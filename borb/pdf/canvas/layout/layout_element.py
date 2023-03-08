#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file contains all the classes needed to perform layout.
This includes an Alignment Enum type, and the base implementation of LayoutElement
"""
import typing
from decimal import Decimal
from enum import Enum

from borb.pdf.canvas.color.color import Color, HexColor
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.line_art.blob_factory import BlobFactory


class Alignment(Enum):
    """
    In typesetting and page layout, alignment or range is the setting of text flow or image placement relative to a page,
    column (measure), table cell, or tab.
    The type alignment setting is sometimes referred to as text alignment,
    text justification, or type justification.
    The edge of a page or column is known as a margin, and a gap between columns is known as a gutter.
    """

    LEFT = 2
    CENTERED = 3
    RIGHT = 5
    JUSTIFIED = 7

    TOP = 11
    MIDDLE = 13
    BOTTOM = 17


class LayoutElement:
    """
    This class contains the common base methods for any object that can be laid out on a Page.
    e.g. the placement of borders, margins, padding, background color, etc
    """

    def __init__(
        self,
        background_color: typing.Optional[Color] = None,
        border_bottom: bool = False,
        border_color: Color = HexColor("000000"),
        border_left: bool = False,
        border_radius_bottom_left: Decimal = Decimal(0),
        border_radius_bottom_right: Decimal = Decimal(0),
        border_radius_top_left: Decimal = Decimal(0),
        border_radius_top_right: Decimal = Decimal(0),
        border_right: bool = False,
        border_top: bool = False,
        border_width: Decimal = Decimal(1),
        font_size: typing.Optional[Decimal] = None,
        horizontal_alignment: Alignment = Alignment.LEFT,
        margin_bottom: typing.Optional[Decimal] = Decimal(0),
        margin_left: typing.Optional[Decimal] = Decimal(0),
        margin_right: typing.Optional[Decimal] = Decimal(0),
        margin_top: typing.Optional[Decimal] = Decimal(0),
        padding_bottom: Decimal = Decimal(0),
        padding_left: Decimal = Decimal(0),
        padding_right: Decimal = Decimal(0),
        padding_top: Decimal = Decimal(0),
        parent: typing.Optional["LayoutElement"] = None,
        vertical_alignment: Alignment = Alignment.TOP,
    ):
        # background color
        self._background_color = background_color

        # borders
        self._border_top = border_top
        self._border_right = border_right
        self._border_bottom = border_bottom
        self._border_left = border_left

        # border radii
        assert (
            border_radius_top_right >= 0
        ), "border_radius_top_right must be a non-negative integer"
        assert (
            border_radius_top_left >= 0
        ), "border_radius_top_left must be a non-negative integer"
        assert (
            border_radius_bottom_left >= 0
        ), "border_radius_bottom_left must be a non-negative integer"
        assert (
            border_radius_bottom_right >= 0
        ), "border_radius_bottom_right must be a non-negative integer"
        self._border_radius_top_left: Decimal = border_radius_top_left
        self._border_radius_top_right: Decimal = border_radius_top_right
        self._border_radius_bottom_right: Decimal = border_radius_bottom_right
        self._border_radius_bottom_left: Decimal = border_radius_bottom_left

        # border width and color
        assert border_width >= 0
        self._border_width = border_width
        self._border_color = border_color

        # font_size
        self._font_size = font_size

        # margin
        assert margin_top is None or margin_top >= 0
        assert margin_right is None or margin_right >= 0
        assert margin_bottom is None or margin_bottom >= 0
        assert margin_left is None or margin_left >= 0
        self._margin_top = margin_top
        self._margin_right = margin_right
        self._margin_bottom = margin_bottom
        self._margin_left = margin_left

        # padding
        assert padding_top >= 0
        assert padding_right >= 0
        assert padding_bottom >= 0
        assert padding_left >= 0
        self._padding_top = padding_top
        self._padding_right = padding_right
        self._padding_bottom = padding_bottom
        self._padding_left = padding_left

        # alignment
        assert horizontal_alignment in [
            Alignment.LEFT,
            Alignment.CENTERED,
            Alignment.RIGHT,
            Alignment.JUSTIFIED,
        ]
        assert vertical_alignment in [Alignment.TOP, Alignment.MIDDLE, Alignment.BOTTOM]
        self._horizontal_alignment = horizontal_alignment
        self._vertical_alignment = vertical_alignment

        # cache
        self._previous_layout_box: typing.Optional[Rectangle] = None
        self._previous_paint_box: typing.Optional[Rectangle] = None

        # linkage (for lists, tables, etc)
        self._parent = parent

    #
    # PRIVATE
    #

    def _get_border_outline(
        self, border_box: Rectangle
    ) -> typing.List[typing.Optional[typing.Tuple[Decimal, Decimal]]]:
        n: int = 0
        xll: Decimal = round(border_box.get_x(), n)
        yll: Decimal = round(border_box.get_y(), n)
        xur: Decimal = round(border_box.get_x() + border_box.get_width(), n)
        yur: Decimal = round(border_box.get_y() + border_box.get_height(), n)

        # top left arc
        points: typing.List[typing.Optional[typing.Tuple[Decimal, Decimal]]] = []
        if self._border_top and self._border_left and self._border_radius_top_left != 0:
            points += [
                (xll, yur - self._border_radius_top_left)
            ] + BlobFactory.smooth_closed_polygon(
                [
                    (xll, yur - self._border_radius_top_left),
                    (xll, yur),
                    (xll + self._border_radius_top_left, yur),
                ],
                2,
            )[
                :-6
            ]
        if self._border_left and self._border_radius_top_left == 0:
            points += [(xll, yur - self._border_radius_top_left)]
            points += [(xll, yur)]
        if self._border_top and self._border_radius_top_left == 0:
            points += [(xll + self._border_radius_top_left, yur)]

        # top
        if self._border_top:
            points += [(xur - self._border_radius_top_right, yur)]
        else:
            points += [None]

        # top right arc
        if (
            self._border_top
            and self._border_right
            and self._border_radius_top_right != 0
        ):
            points += BlobFactory.smooth_closed_polygon(
                [
                    (xur - self._border_radius_top_right, yur),
                    (xur, yur),
                    (xur, yur - self._border_radius_top_right),
                ],
                2,
            )[:-6]
        if self._border_top and self._border_radius_top_right == 0:
            points += [(xur, yur)]
        if self._border_right and self._border_radius_top_right == 0:
            points += [(xur, yur - self._border_radius_top_right)]

        # right
        if self._border_right:
            points += [(xur, yll + self._border_radius_bottom_right)]
        else:
            points += [None]

        # bottom right arc
        if (
            self._border_bottom
            and self._border_right
            and self._border_radius_bottom_right != 0
        ):
            points += BlobFactory.smooth_closed_polygon(
                [
                    (xur, yll + self._border_radius_bottom_right),
                    (xur, yll),
                    (xur - self._border_radius_bottom_right, yll),
                ],
                2,
            )[:-6]
        if self._border_right and self._border_radius_bottom_right == 0:
            points += [(xur, yll)]
        if self._border_bottom and self._border_radius_bottom_right == 0:
            points += [(xur - self._border_radius_bottom_right, yll)]

        # bottom
        if self._border_bottom:
            points += [(xll + self._border_radius_bottom_left, yll)]
        else:
            points += [None]

        # bottom left arc
        if (
            self._border_bottom
            and self._border_left
            and self._border_radius_bottom_left != 0
        ):
            points += BlobFactory.smooth_closed_polygon(
                [
                    (xll + self._border_radius_bottom_left, yll),
                    (xll, yll),
                    (xll, yll + self._border_radius_bottom_left),
                ],
                2,
            )[:-6]
        if self._border_bottom and self._border_radius_bottom_left == 0:
            points += [(xll, yll)]
        if self._border_left and self._border_radius_bottom_left == 0:
            points += [(xll, yll + self._border_radius_bottom_right)]

        # left
        if self._border_left:
            points += [(xll, yur - self._border_radius_top_left)]
        else:
            points += [None]

        # return
        return points

    def _get_content_box(self, available_space: Rectangle) -> Rectangle:
        return Rectangle(
            available_space.get_x(),
            available_space.get_y() + available_space.get_height(),
            Decimal(0),
            Decimal(0),
        )

    def _needs_to_be_tagged(self, p: "Page") -> bool:  # type: ignore[name-defined]
        """
        This function returns whether this LayoutElement needs to be tagged
        :param p:   the Page on which this LayoutElement is to be painted
        :return:    true if this LayoutElement needs to be tagged, False otherwise
        """
        document: typing.Optional["Document"] = p.get_document()  # type: ignore[name-defined]
        if document is None:
            return False
        # fmt: off
        conformance_level: typing.Optional["ConformanceLevel"] = document.get_document_info().get_conformance_level_upon_create()   # type: ignore[name-defined]
        if conformance_level is None:
            return False
        return conformance_level.get_conformance_level() in ["A", "U"]
        # fmt: on

    def _paint_background(
        self, page: "Page", background_box: Rectangle  # type: ignore[name-defined]
    ):
        if not self._background_color:
            return
        assert self._background_color
        rgb_color = self._background_color.to_rgb()

        # easy case
        if (
            self._border_radius_top_right == 0
            and self._border_radius_top_left == 0
            and self._border_radius_bottom_left == 0
            and self._border_radius_bottom_right == 0
        ):

            # fmt: off
            content = """
                q %f %f %f rg %f %f m
                %f %f l
                %f %f l
                %f %f l
                %f %f l
                f
                Q
                """ % (
                float(rgb_color.red),
                float(rgb_color.green),
                float(rgb_color.blue),
                background_box.get_x(),                                 # ul_x
                background_box.get_y() + background_box.get_height(),   # ul_y

                background_box.get_x() + background_box.get_width(),    # ur_x
                background_box.get_y() + background_box.get_height(),   # ur_y

                background_box.get_x() + background_box.get_width(),    # lr_x
                background_box.get_y(),                                 # lr_y

                background_box.get_x(),                                 # ll_x
                background_box.get_y(),                                 # ll_y

                background_box.get_x(),                                 # ul_x
                background_box.get_y() + background_box.get_height(),   # ul_y
            )
            # fmt: on
            page.append_to_content_stream(content)
            return

        # remember border state
        before = [
            self._border_top,
            self._border_right,
            self._border_bottom,
            self._border_left,
        ]

        # set all borders
        self._border_top = True
        self._border_right = True
        self._border_bottom = True
        self._border_left = True

        # get outline
        outline_points = self._get_border_outline(background_box)
        assert outline_points[0] is not None

        # restore all borders
        self._border_top = before[0]
        self._border_right = before[1]
        self._border_bottom = before[2]
        self._border_left = before[3]

        # write
        content = """
            q %f %f %f rg %f %f m
            """ % (
            float(rgb_color.red),
            float(rgb_color.green),
            float(rgb_color.blue),
            float(outline_points[0][0]),
            float(outline_points[0][1]),
        )
        for p in outline_points:
            assert p is not None
            content += " %f %f l" % (float(p[0]), float(p[1]))
        content += " f Q"
        page.append_to_content_stream(content)

    def _paint_borders(self, page: "Page", border_box: Rectangle):  # type: ignore[name-defined]
        # border is not wanted on any side
        if (
            self._border_top
            == self._border_right
            == self._border_bottom
            == self._border_left
            == False
        ):
            return

        # border width is set to zero
        if self._border_width == 0:
            return

        # draw border(s)
        rgb_color = self._border_color.to_rgb()
        content = "q %f %f %f RG %f w " % (
            float(rgb_color.red),
            float(rgb_color.green),
            float(rgb_color.blue),
            float(self._border_width),
        )

        # turn points into lines
        points = self._get_border_outline(border_box)
        for i, p in enumerate(points[:-1]):
            p0: typing.Optional[typing.Tuple[Decimal, Decimal]] = p
            p1: typing.Optional[typing.Tuple[Decimal, Decimal]] = points[i + 1]
            if p0 is None or p1 is None:
                continue
            content += " %d %d m %d %d l s" % (
                float(p0[0]),
                float(p0[1]),
                float(p1[0]),
                float(p1[1]),
            )
        content += " Q"
        page.append_to_content_stream(content)

    def _paint_content_box(self, page: "Page", content_box: Rectangle) -> None:  # type: ignore[name-defined]
        pass

    #
    # PUBLIC
    #

    def get_font_size(self) -> Decimal:
        """
        This function returns the font size of this LayoutElement
        """
        return self._font_size or Decimal(0)

    def get_layout_box(self, available_space: Rectangle):
        """
        This function returns the previous result of layout
        :return:    the Rectangle that was the result of the previous layout operation
        """
        horizontal_border_width: Decimal = Decimal(0)
        if self._border_left:
            horizontal_border_width += self._border_width
        if self._border_right:
            horizontal_border_width += self._border_width

        vertical_border_width: Decimal = Decimal(0)
        if self._border_top:
            vertical_border_width += self._border_width
        if self._border_bottom:
            vertical_border_width += self._border_width

        cbox_available_space: Rectangle = Rectangle(
            available_space.get_x()
            + self._padding_left
            + (self._border_width if self._border_left else Decimal(0)),
            available_space.get_y()
            + self._padding_bottom
            + (self._border_width if self._border_bottom else Decimal(0)),
            max(
                Decimal(0),
                available_space.get_width()
                - self._padding_left
                - self._padding_right
                - horizontal_border_width,
            ),
            max(
                Decimal(0),
                available_space.get_height()
                - self._padding_top
                - self._padding_bottom
                - vertical_border_width,
            ),
        )

        # determine content_box
        cbox: Rectangle = self._get_content_box(cbox_available_space)

        # take into account vertical_alignment
        delta_x: Decimal = Decimal(0)
        delta_y: Decimal = Decimal(0)
        if self._vertical_alignment == Alignment.MIDDLE:
            delta_y = (cbox_available_space.get_height() - cbox.get_height()) / Decimal(
                2
            )
            cbox.y -= delta_y
        if self._vertical_alignment == Alignment.BOTTOM:
            delta_y = cbox_available_space.get_height() - cbox.get_height()
            cbox.y -= delta_y

        # take into account horizontal_alignment
        if self._horizontal_alignment == Alignment.CENTERED:
            delta_x = (cbox_available_space.get_width() - cbox.get_width()) / Decimal(2)
            cbox.x += delta_x
        if self._horizontal_alignment == Alignment.RIGHT:
            delta_x = cbox_available_space.get_width() - cbox.get_width()
            cbox.x += delta_x

        # return
        # fmt: off
        self._previous_layout_box = Rectangle(
            cbox.get_x() - self._padding_left - (self._border_width if self._border_left else Decimal(0)),
            cbox.get_y() - self._padding_bottom - (self._border_width if self._border_bottom else Decimal(0)),
            cbox.get_width() + self._padding_left + self._padding_right + horizontal_border_width,
            cbox.get_height() + self._padding_top + self._padding_bottom + vertical_border_width,
        )
        # fmt: on
        return self._previous_layout_box

    def get_margin_bottom(self) -> Decimal:
        """
        This function returns the bottom margin of this LayoutElement
        """
        return self._margin_bottom or Decimal(0)

    def get_margin_left(self) -> Decimal:
        """
        This function returns the left margin of this LayoutElement
        """
        return self._margin_left or Decimal(0)

    def get_margin_right(self) -> Decimal:
        """
        This function returns the right margin of this LayoutElement
        """
        return self._margin_right or Decimal(0)

    def get_margin_top(self) -> Decimal:
        """
        This function returns the top margin of this LayoutElement
        """
        return self._margin_top or Decimal(0)

    def get_previous_layout_box(self) -> typing.Optional[Rectangle]:
        """
        This function returns the previous result of layout of this LayoutElement
        :return:    the Rectangle that was the result of the previous layout operation
        """
        return self._previous_layout_box

    def get_previous_paint_box(self) -> typing.Optional[Rectangle]:
        """
        This function returns the previous result of painting this LayoutElement
        :return:    the Rectangle that was the result of the previous paint operation
        """
        return self._previous_paint_box

    def paint(self, page: "Page", available_space: Rectangle) -> None:  # type: ignore[name-defined]
        """
        This method paints this LayoutElement on the given Page, in the available space
        :param page:                the Page on which to paint this LayoutElement
        :param available_space:     the available space (as a Rectangle) on which to paint this LayoutElement
        :return:                    None
        """

        # calculate horizontal_border_width
        horizontal_border_width: Decimal = Decimal(0)
        if self._border_left:
            horizontal_border_width += self._border_width
        if self._border_right:
            horizontal_border_width += self._border_width

        # calculate vertical_border_width
        vertical_border_width: Decimal = Decimal(0)
        if self._border_top:
            vertical_border_width += self._border_width
        if self._border_bottom:
            vertical_border_width += self._border_width

        cbox_available_space: Rectangle = Rectangle(
            available_space.get_x()
            + self._padding_left
            + (self._border_width if self._border_left else Decimal(0)),
            available_space.get_y()
            + self._padding_bottom
            + (self._border_width if self._border_bottom else Decimal(0)),
            max(
                Decimal(0),
                available_space.get_width()
                - self._padding_left
                - self._padding_right
                - horizontal_border_width,
            ),
            max(
                Decimal(0),
                available_space.get_height()
                - self._padding_top
                - self._padding_bottom
                - vertical_border_width,
            ),
        )

        # determine content_box
        cbox: Rectangle = self._get_content_box(cbox_available_space)

        # take into account vertical_alignment
        delta_x: Decimal = Decimal(0)
        delta_y: Decimal = Decimal(0)
        if self._vertical_alignment == Alignment.MIDDLE:
            delta_y = (cbox_available_space.get_height() - cbox.get_height()) / Decimal(
                2
            )
            cbox.y -= delta_y
        if self._vertical_alignment == Alignment.BOTTOM:
            delta_y = cbox_available_space.get_height() - cbox.get_height()
            cbox.y -= delta_y

        # take into account horizontal_alignment
        if self._horizontal_alignment == Alignment.CENTERED:
            delta_x = (cbox_available_space.get_width() - cbox.get_width()) / Decimal(2)
            cbox.x += delta_x
        if self._horizontal_alignment == Alignment.RIGHT:
            delta_x = cbox_available_space.get_width() - cbox.get_width()
            cbox.x += delta_x

        # paint the background first
        bgbox: Rectangle = Rectangle(
            cbox.get_x()
            - self._padding_left
            - (self._border_width if self._border_left else Decimal(0)),
            cbox.get_y()
            - self._padding_bottom
            - (self._border_width if self._border_bottom else Decimal(0)),
            cbox.get_width()
            + self._padding_left
            + self._padding_right
            + horizontal_border_width,
            cbox.get_height()
            + self._padding_top
            + self._padding_bottom
            + vertical_border_width,
        )
        self._paint_background(page, bgbox)

        # paint the borders
        self._paint_borders(page, bgbox)

        # paint the actual content
        self._paint_content_box(page, cbox)

        # set bounding box
        self._previous_paint_box = bgbox
