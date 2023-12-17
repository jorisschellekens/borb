#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In Euclidean plane geometry, a rectangle is a quadrilateral with four right angles.
"""
from decimal import Decimal


class Rectangle:
    """
    In Euclidean plane geometry, a rectangle is a quadrilateral with four right angles.
    It can also be defined as an equiangular quadrilateral, since equiangular means that all of its angles are equal (360°/4 = 90°).
    It can also be defined as a parallelogram containing a right angle. A rectangle with four sides of equal length is a square.
    The term oblong is occasionally used to refer to a non-square rectangle.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(
        self,
        lower_left_x: Decimal,
        lower_left_y: Decimal,
        width: Decimal,
        height: Decimal,
    ):
        # TODO: sort args
        assert width >= 0, "A Rectangle must have a non-negative width."
        assert height >= 0, "A Rectangle must have a non-negative height."
        self.x = lower_left_x
        self.y = lower_left_y
        self.width = width
        self.height = height

    #
    # PRIVATE
    #

    def __hash__(self):
        attr_hash_for_layout: int = 1927868237
        for a in [int(self.x), int(self.y), int(self.width), int(self.height)]:
            h: int = hash(a)
            attr_hash_for_layout ^= (h ^ (h << 16) ^ 89869747) * 3644798167
        return attr_hash_for_layout * 69069 + 907133923

    #
    # PUBLIC
    #

    def circumference_contains(self, x: Decimal, y: Decimal) -> bool:
        """
        This function returns True if the circumference of this Rectangle contains the given point
        False otherwise
        """
        return x in [self.x, self.x + self.width] and y in [
            self.y,
            self.y + self.height,
        ]

    def contains(self, x: Decimal, y: Decimal) -> bool:
        """
        This function returns True if this Rectangle contains the given point
        False otherwise
        """
        return self.x <= x <= (self.x + self.width) and self.y <= y <= (
            self.y + self.height
        )

    def get_height(self) -> Decimal:
        """
        This function returns the height of this Rectangle
        """
        return self.height

    def get_width(self) -> Decimal:
        """
        This function returns the width of this Rectangle
        """
        return self.width

    def get_x(self) -> Decimal:
        """
        This function returns the x-coordinate of the lower-left of this Rectangle
        """
        return self.x

    def get_y(self) -> Decimal:
        """
        This function returns the y-coordinate of the lower-left of this Rectangle
        """
        return self.y

    def grow(self, amount: Decimal) -> "Rectangle":
        """
        This function returns a (slightly) larger Rectangle,
        grown by the given amount
        """
        assert amount >= 0
        return Rectangle(
            self.x - amount,
            self.y - amount,
            self.width + Decimal(2) * amount,
            self.height + Decimal(2) * amount,
        )

    def intersects(self, other_rectangle: "Rectangle") -> bool:
        """
        This function returns True if this Rectangle intersects with the given Rectangle,
        False otherwise
        """
        # fmt: off
        x_intersect: bool = (other_rectangle.x <= self.x <= (other_rectangle.x + other_rectangle.width))
        x_intersect = x_intersect or (self.x <= other_rectangle.x <= (self.x + self.width))
        y_intersect: bool = (other_rectangle.y <= self.y <= (other_rectangle.y + other_rectangle.height))
        y_intersect = y_intersect or (self.y <= other_rectangle.y <= (self.y + self.height))
        # fmt: on
        return x_intersect and y_intersect

    def shrink(self, amount: Decimal) -> "Rectangle":
        """
        This function returns a (slightly) smaller Rectangle,
        shrunk by the given amount
        """
        assert amount >= 0
        return Rectangle(
            self.x + amount,
            self.y + amount,
            self.width - Decimal(2) * amount,
            self.height - Decimal(2) * amount,
        )
