import math
import typing
from decimal import Decimal
from typing import Tuple

from ptext.pdf.canvas.geometry.rectangle import Rectangle


class LineArtFactory:
    @staticmethod
    def right_sided_triangle(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
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
        return LineArtFactory.regular_n_gon(bounding_box, 3)

    @staticmethod
    def parallelogram(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
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
        return LineArtFactory.regular_n_gon(bounding_box, 5)

    @staticmethod
    def hexagon(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        return LineArtFactory.regular_n_gon(bounding_box, 6)

    @staticmethod
    def heptagon(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        return LineArtFactory.regular_n_gon(bounding_box, 7)

    @staticmethod
    def octagon(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        return LineArtFactory.regular_n_gon(bounding_box, 8)

    @staticmethod
    def fraction_of_circle(
        bounding_box: Rectangle,
        fraction: Decimal,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
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
        return LineArtFactory.fraction_of_circle(bounding_box, Decimal(0.75))

    @staticmethod
    def half_of_circle(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
        return LineArtFactory.fraction_of_circle(bounding_box, Decimal(0.5))

    @staticmethod
    def droplet(bounding_box: Rectangle) -> typing.List[Tuple[Decimal, Decimal]]:
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
        return LineArtFactory.n_pointed_star(bounding_box, 4)

    @staticmethod
    def five_pointed_star(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        return LineArtFactory.n_pointed_star(bounding_box, 5)

    @staticmethod
    def six_pointed_star(
        bounding_box: Rectangle,
    ) -> typing.List[Tuple[Decimal, Decimal]]:
        return LineArtFactory.n_pointed_star(bounding_box, 6)

    @staticmethod
    def n_pointed_star(
        bounding_box: Rectangle, n: int
    ) -> typing.List[Tuple[Decimal, Decimal]]:
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
