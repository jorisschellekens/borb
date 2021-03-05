#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class provides static convenience methods for generating points of common line-art in electronic documents,
    such as arrows, rectangles, triangles, regular n-gons, stars, etc
"""
import math
import typing
from decimal import Decimal
from typing import Tuple

from ptext.pdf.canvas.geometry.rectangle import Rectangle


class LineArtFactory:
    """
    This class provides static convenience methods for generating points of common line-art in electronic documents,
    such as arrows, rectangles, triangles, regular n-gons, stars, etc
    """

    @staticmethod
    def dragon_curve(
        bounding_box: Rectangle, number_of_iterations: int = 10
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for the Heighway dragon (also known as the Harter–Heighway dragon,
        or the Jurassic Park dragon) curve that fits in the given bounding box
        """
        seq: typing.List[int] = [1]
        for _ in range(0, number_of_iterations):
            seq.append(1)
            m: int = int(len(seq) / 2) - 1
            for i, v in enumerate(seq[0:-1]):
                if i == m:
                    seq.append(1 - v)
                else:
                    seq.append(v)
        step_size = Decimal(10)
        direction: int = 0
        x: Decimal = Decimal(0)
        y: Decimal = Decimal(0)
        points: typing.List[Tuple[Decimal, Decimal]] = []
        for turn in seq:
            # go forward
            if direction == 0:
                y += step_size
            elif direction == 1:
                x += step_size
            elif direction == 2:
                y -= step_size
            elif direction == 3:
                x -= step_size
            # store point
            points.append((x, y))
            # make turn
            if turn == 0:
                direction = (direction + 1) % 4
            elif turn == 1:
                direction = (direction + 3) % 4

        # determine width/height
        w: Decimal = max([x[0] for x in points]) - min([x[0] for x in points])
        h: Decimal = max([x[1] for x in points]) - min([x[1] for x in points])

        # scale everything
        w_scale: Decimal = bounding_box.width / w
        h_scale: Decimal = bounding_box.height / h
        points = [(x[0] * w_scale, x[1] * h_scale) for x in points]

        # translate everything
        x_delta: Decimal = x - bounding_box.x
        y_delta: Decimal = y - bounding_box.y
        points = [(x[0] - x_delta, x[1] - y_delta) for x in points]

        return points

    @staticmethod
    def cross(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a cross that matches the given bounding box
        """
        return [
            (bounding_box.x, bounding_box.y + bounding_box.height * Decimal(0.66)),
            (
                bounding_box.x + bounding_box.width * Decimal(0.33),
                bounding_box.y + bounding_box.height * Decimal(0.66),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.33),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.66),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.66),
                bounding_box.y + bounding_box.height * Decimal(0.66),
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * Decimal(0.66),
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * Decimal(0.33),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.66),
                bounding_box.y + bounding_box.height * Decimal(0.33),
            ),
            (bounding_box.x + bounding_box.width * Decimal(0.66), bounding_box.y),
            (bounding_box.x + bounding_box.width * Decimal(0.33), bounding_box.y),
            (
                bounding_box.x + bounding_box.width * Decimal(0.33),
                bounding_box.y + bounding_box.height * Decimal(0.33),
            ),
            (bounding_box.x, bounding_box.y + bounding_box.height * Decimal(0.33)),
            # repeat first point to explicitly close shape
            (bounding_box.x, bounding_box.y + bounding_box.height * Decimal(0.66)),
        ]

    @staticmethod
    def cartoon_diamond(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a cartoon diamond that matches the given bounding box
        """
        top_ratio: Decimal = Decimal(0.75)
        return [
            (bounding_box.x + bounding_box.width * Decimal(0.5), bounding_box.y),
            (bounding_box.x, bounding_box.y + bounding_box.height * top_ratio),
            (
                bounding_box.x + bounding_box.width * Decimal(0.2),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.4),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.33),
                bounding_box.y + bounding_box.height * top_ratio,
            ),
            (bounding_box.x + bounding_box.width * Decimal(0.5), bounding_box.y),
            (
                bounding_box.x + bounding_box.width * Decimal(0.66),
                bounding_box.y + bounding_box.height * top_ratio,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.6),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.4),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.8),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * top_ratio,
            ),
            (bounding_box.x, bounding_box.y + bounding_box.height * top_ratio),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * top_ratio,
            ),
            # repeat first point to explicitly close shape
            (bounding_box.x + bounding_box.width * Decimal(0.5), bounding_box.y),
        ]

    @staticmethod
    def rectangle(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a rectangle that matches the given bounding box
        """
        return [
            (bounding_box.x, bounding_box.y),
            (bounding_box.x + bounding_box.width, bounding_box.y),
            (bounding_box.x + bounding_box.width, bounding_box.y + bounding_box.height),
            (bounding_box.x, bounding_box.y + bounding_box.height),
            # repeat first point to explicitly close shape
            (bounding_box.x, bounding_box.y),
        ]

    @staticmethod
    def right_angled_triangle(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a right-angled triangle that fits in the given bounding box
        """
        return [
            (bounding_box.x, bounding_box.y),
            (bounding_box.x + bounding_box.width, bounding_box.y),
            (bounding_box.x, bounding_box.y + bounding_box.height),
            # repeat first point to explicitly close shape
            (bounding_box.x, bounding_box.y),
        ]

    @staticmethod
    def regular_n_gon(
        bounding_box: Rectangle, n: int
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a regular n-gon that fits in the given bounding box
        """
        r = min(bounding_box.width, bounding_box.height) / Decimal(2)
        mid_x = bounding_box.x + r
        mid_y = bounding_box.y + r
        points = []
        for i in range(0, 360, int(360 / n)):
            x = Decimal(math.sin(math.radians(i))) * r + mid_x
            y = Decimal(math.cos(math.radians(i))) * r + mid_y
            points.append((x, y))
        points.append(points[0])
        return points

    @staticmethod
    def isosceles_triangle(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for an isosceles triangle that fits in the given bounding box
        """
        return LineArtFactory.regular_n_gon(bounding_box, 3)

    @staticmethod
    def parallelogram(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a parallelogram that fits in the given bounding box
        """
        return [
            (bounding_box.x, bounding_box.y),
            (
                bounding_box.x + bounding_box.width * Decimal(0.75),
                bounding_box.y,
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.25),
                bounding_box.y + bounding_box.height,
            ),
            # repeat first point to explicitly close shape
            (bounding_box.x, bounding_box.y),
        ]

    @staticmethod
    def trapezoid(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a trapezoid that fits in the given bounding box
        """
        return [
            (bounding_box.x, bounding_box.y),
            (bounding_box.x + bounding_box.width, bounding_box.y),
            (
                bounding_box.x + bounding_box.width * Decimal(0.75),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.25),
                bounding_box.y + bounding_box.height,
            ),
            # repeat first point to explicitly close shape
            (bounding_box.x, bounding_box.y),
        ]

    @staticmethod
    def diamond(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a diomond that fits in the given bounding box
        """
        HALF: Decimal = Decimal(0.5)
        return [
            (
                bounding_box.x + bounding_box.width * HALF,
                bounding_box.y,
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * HALF,
            ),
            (
                bounding_box.x + bounding_box.width * HALF,
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x,
                bounding_box.y + bounding_box.height * HALF,
            ),
            # repeat first point to explicitly close shape
            (
                bounding_box.x + bounding_box.width * HALF,
                bounding_box.y,
            ),
        ]

    @staticmethod
    def pentagon(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a pentagon that fits in the given bounding box
        """
        return LineArtFactory.regular_n_gon(bounding_box, 5)

    @staticmethod
    def hexagon(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a hexagon that fits in the given bounding box
        """
        return LineArtFactory.regular_n_gon(bounding_box, 6)

    @staticmethod
    def heptagon(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a heptagon that fits in the given bounding box
        """
        return LineArtFactory.regular_n_gon(bounding_box, 7)

    @staticmethod
    def octagon(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for an octagon that fits in the given bounding box
        """
        return LineArtFactory.regular_n_gon(bounding_box, 8)

    @staticmethod
    def fraction_of_circle(
        bounding_box: Rectangle,
        fraction: Decimal,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a circle-slice that fits in the given bounding box
        """
        r = Decimal(min(bounding_box.width, bounding_box.height)) / Decimal(2)
        mid_x = bounding_box.x + r
        mid_y = bounding_box.y + r
        points: typing.List[Tuple[Decimal, Decimal]] = []
        for i in range(0, int(360 * float(fraction))):
            x = Decimal(math.sin(math.radians(i))) * r + mid_x
            y = Decimal(math.cos(math.radians(i))) * r + mid_y
            points.append((x, y))
        points.append((mid_x, mid_y))
        # repeat first point to explicitly close shape
        points.append(points[0])
        return points

    @staticmethod
    def three_quarters_of_circle(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a circle-slice of 270 degrees that fits in the given bounding box
        """
        return LineArtFactory.fraction_of_circle(bounding_box, Decimal(0.75))

    @staticmethod
    def half_of_circle(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a circle-slice of 180 degrees that fits in the given bounding box
        """
        return LineArtFactory.fraction_of_circle(bounding_box, Decimal(0.5))

    @staticmethod
    def droplet(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a droplet that fits in the given bounding box
        """
        r = Decimal(min(bounding_box.width, bounding_box.height)) / Decimal(2)
        mid_x = bounding_box.x + r
        mid_y = bounding_box.y + r
        points: typing.List[Tuple[Decimal, Decimal]] = []
        for i in range(0, 270):
            x = Decimal(math.sin(math.radians(i))) * r + mid_x
            y = Decimal(math.cos(math.radians(i))) * r + mid_y
            points.append((x, y))
        points.append((points[-1][0], points[0][1]))
        # repeat first point to explicitly close shape
        points.append(points[0])
        return points

    @staticmethod
    def four_pointed_star(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a four point star that fits in the given bounding box
        """
        return LineArtFactory.n_pointed_star(bounding_box, 4)

    @staticmethod
    def five_pointed_star(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a five point star that fits in the given bounding box
        """
        return LineArtFactory.n_pointed_star(bounding_box, 5)

    @staticmethod
    def six_pointed_star(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a six point star that fits in the given bounding box
        """
        return LineArtFactory.n_pointed_star(bounding_box, 6)

    @staticmethod
    def n_pointed_star(
        bounding_box: Rectangle, n: int
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for an n-point star that fits in the given bounding box
        """
        assert n >= 3
        r = min(bounding_box.width, bounding_box.height) / Decimal(2)
        mid_x = bounding_box.x + r
        mid_y = bounding_box.y + r
        inner_radius = r * Decimal(0.39)
        points: typing.List[Tuple[Decimal, Decimal]] = []
        for i in range(0, 360, int(360 / n)):
            # outer point
            x = Decimal(math.sin(math.radians(i))) * r + mid_x
            y = Decimal(math.cos(math.radians(i))) * r + mid_y
            points.append((x, y))
            # inner point
            half_angle = int(360 / (2 * n))
            x = Decimal(math.sin(math.radians(i + half_angle))) * inner_radius + mid_x
            y = Decimal(math.cos(math.radians(i + half_angle))) * inner_radius + mid_y
            points.append((x, y))
        points.append(points[0])
        return points

    @staticmethod
    def arrow_left(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for an arrow pointing left that fits in the given bounding box
        """
        return [
            (
                bounding_box.x,
                bounding_box.y + bounding_box.width * Decimal(0.5),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.39),
                bounding_box.y,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.39),
                bounding_box.y + bounding_box.height * Decimal(0.2),
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * Decimal(0.2),
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * Decimal(0.8),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.39),
                bounding_box.y + bounding_box.height * Decimal(0.8),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.39),
                bounding_box.y + bounding_box.height,
            ),
            # repeat first point to explicitly close shape
            (
                bounding_box.x,
                bounding_box.y + bounding_box.width * Decimal(0.5),
            ),
        ]

    @staticmethod
    def arrow_right(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for an arrow pointing right that fits in the given bounding box
        """
        return [
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.width * Decimal(0.5),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.61),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.61),
                bounding_box.y + bounding_box.height * Decimal(0.8),
            ),
            (
                bounding_box.x,
                bounding_box.y + bounding_box.height * Decimal(0.8),
            ),
            (
                bounding_box.x,
                bounding_box.y + bounding_box.height * Decimal(0.2),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.61),
                bounding_box.y + bounding_box.height * Decimal(0.2),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.61),
                bounding_box.y,
            ),
            # repeat first point to explicitly close shape
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.width * Decimal(0.5),
            ),
        ]

    @staticmethod
    def arrow_up(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for an arrow pointing up that fits in the given bounding box
        """
        return [
            (
                bounding_box.x + bounding_box.width * Decimal(0.5),
                bounding_box.y + bounding_box.height,
            ),
            (bounding_box.x, bounding_box.y + bounding_box.height * Decimal(0.61)),
            (
                bounding_box.x + bounding_box.width * Decimal(0.2),
                bounding_box.y + bounding_box.height * Decimal(0.61),
            ),
            (bounding_box.x + bounding_box.width * Decimal(0.2), bounding_box.y),
            (bounding_box.x + bounding_box.width * Decimal(0.8), bounding_box.y),
            (
                bounding_box.x + bounding_box.width * Decimal(0.8),
                bounding_box.y + bounding_box.height * Decimal(0.61),
            ),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * Decimal(0.61),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.5),
                bounding_box.y + bounding_box.height,
            ),
        ]

    @staticmethod
    def arrow_down(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for an arrow pointing down that fits in the given bounding box
        """
        return [
            (bounding_box.x + bounding_box.width * Decimal(0.5), bounding_box.y),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * Decimal(0.39),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.8),
                bounding_box.y + bounding_box.height * Decimal(0.39),
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.8),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.2),
                bounding_box.y + bounding_box.height,
            ),
            (
                bounding_box.x + bounding_box.width * Decimal(0.2),
                bounding_box.y + bounding_box.height * Decimal(0.39),
            ),
            (bounding_box.x, bounding_box.y + bounding_box.height * Decimal(0.39)),
            (bounding_box.x + bounding_box.width * Decimal(0.5), bounding_box.y),
        ]

    @staticmethod
    def heart(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a heart that fits in the given bounding box
        """
        r = min(bounding_box.width, bounding_box.height) / Decimal(2)
        points: typing.List[Tuple[Decimal, Decimal]] = []
        # first arc
        for i in range(0, 180):
            x = (
                Decimal(math.sin(math.radians(i - 90))) * r * Decimal(0.5)
                + bounding_box.x
                + r * Decimal(0.5)
            )
            y = (
                Decimal(math.cos(math.radians(i - 90))) * r * Decimal(0.5)
                + bounding_box.y
                + r
            )
            points.append((x, y))
        midpoint = points[-1]
        # second arc
        for i in range(0, 180):
            x = (
                Decimal(math.sin(math.radians(i - 90))) * r * Decimal(0.5)
                + bounding_box.x
                + r * Decimal(1.5)
            )
            y = (
                Decimal(math.cos(math.radians(i - 90))) * r * Decimal(0.5)
                + bounding_box.y
                + r
            )
            points.append((x, y))
        # triangle
        points.append((midpoint[0], bounding_box.y))
        points.append(points[0])
        return points

    @staticmethod
    def sticky_note(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        """
        This function returns the coordinates for a sticky note that fits in the given bounding box
        """
        turn_up: Decimal = Decimal(0.10)
        turn_up_inv: Decimal = Decimal(1) - turn_up
        return [
            (bounding_box.x, bounding_box.y),
            (bounding_box.x, bounding_box.y + bounding_box.height),
            (bounding_box.x + bounding_box.width, bounding_box.y + bounding_box.height),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * turn_up,
            ),
            (
                bounding_box.x + bounding_box.width * turn_up_inv,
                bounding_box.y + bounding_box.height * turn_up,
            ),
            (bounding_box.x + bounding_box.width * turn_up_inv, bounding_box.y),
            (
                bounding_box.x + bounding_box.width,
                bounding_box.y + bounding_box.height * turn_up,
            ),
            (bounding_box.x + bounding_box.width * turn_up_inv, bounding_box.y),
            # repeat first point to explicitly close shape
            (bounding_box.x, bounding_box.y),
        ]
