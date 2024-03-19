#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This class represents a line segment
"""
import typing
from decimal import Decimal
import math

from borb.pdf.canvas.geometry.matrix import Matrix


class LineSegment:
    """
    This class represents a line segment
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self, x0: Decimal, y0: Decimal, x1: Decimal, y1: Decimal):
        self.x0: Decimal = x0
        self.y0: Decimal = y0
        self.x1: Decimal = x1
        self.y1: Decimal = y1

    #
    # PRIVATE
    #

    #
    # PUBLIC
    #

    def get_end(self) -> typing.Tuple[Decimal, Decimal]:
        """
        This function returns the end of this LineSegment
        :return:    the end (second point) of this LineSegment
        """
        return (self.x1, self.y1)

    def get_start(self) -> typing.Tuple[Decimal, Decimal]:
        """
        This function returns the start of this LineSegment
        :return:    the start (first point) of this LineSegment
        """
        return (self.x0, self.y0)

    def length(self) -> Decimal:
        """
        This function returns the length of this LineSegment
        :return:    the length of this LineSegment
        """
        return Decimal(math.sqrt((self.x0 - self.x1) ** 2 + (self.y0 - self.y1) ** 2))

    def transform_by(self, matrix: Matrix) -> "LineSegment":
        """
        This function transforms the start and end of this LineSegment by a given Matrix,
        it returns the transformed LineSegment
        :param matrix:  the matrix to transform by
        :return:        a new (transformed) LineSegment
        """
        p0 = matrix.cross(self.x0, self.y0, Decimal(1))
        p1 = matrix.cross(self.x1, self.y1, Decimal(1))
        return LineSegment(p0[0], p0[1], p1[0], p1[1])
