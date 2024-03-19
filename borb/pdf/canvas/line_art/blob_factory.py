#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This class provides static convenience methods for generating a stylistic blob
"""
import random
import typing
from decimal import Decimal
import math


class BlobFactory:
    """
    This class provides static convenience methods for generating a stylistic blob
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def _check_if_object_is_polygon(
        points: typing.List[typing.Tuple[Decimal, Decimal]]
    ):
        if points[0] == points[len(points) - 1]:
            return True
        else:
            return False

    @staticmethod
    def _multiply_point(
        multiplier: Decimal, P: typing.Tuple[Decimal, Decimal]
    ) -> typing.Tuple[Decimal, Decimal]:
        x, y = P
        return Decimal(x * multiplier), Decimal(y * multiplier)

    @staticmethod
    def _q_point(P1, P2):
        summand1 = BlobFactory._multiply_point(Decimal(0.75), P1)
        summand2 = BlobFactory._multiply_point(Decimal(0.25), P2)
        Q = BlobFactory._sum_points(summand1, summand2)
        return Q

    @staticmethod
    def _r_point(P1, P2):
        summand1 = BlobFactory._multiply_point(Decimal(0.25), P1)
        summand2 = BlobFactory._multiply_point(Decimal(0.75), P2)
        R = BlobFactory._sum_points(summand1, summand2)
        return R

    @staticmethod
    def _sum_points(
        P1: typing.Tuple[Decimal, Decimal], P2: typing.Tuple[Decimal, Decimal]
    ) -> typing.Tuple[Decimal, Decimal]:
        x1, y1 = P1
        x2, y2 = P2
        return x1 + x2, y1 + y2

    #
    # PUBLIC
    #

    @staticmethod
    def blob(number_of_edges: int) -> typing.List[typing.Tuple[Decimal, Decimal]]:
        """
        This function returns a smoothed n-sided blob shape
        :param number_of_edges:     the number of "edges" the blob should have
        :return:                    the coordinates of the perimeter of the blob
        """

        # generate regular polygon
        points = [
            (Decimal(math.cos(math.radians(x))), Decimal(math.sin(math.radians(x))))
            for x in range(0, 360, int(360 / number_of_edges))
        ]

        # randomly distort polygon
        random_radius = [Decimal(random.randint(1, 10)) for _ in range(0, len(points))]
        points = [(p[0] * r, p[1] * r) for p, r in zip(points, random_radius)]

        # smoothing
        while len(points) < 1024:
            points = BlobFactory.smooth_closed_polygon(points, 2)
        points.append(points[0])

        # return
        return points

    @staticmethod
    def smooth_closed_polygon(
        points: typing.List[typing.Tuple[Decimal, Decimal]], number_of_refinements: int
    ):
        """
        This function smooths a polygon by using Chaikin's algorithm.
        In 1974, George Chaikin gave a lecture at the University of Utah in which he specified a novel
        procedure for generating curves from a limited number of points. This algorithm is interesting as it was
        one of the first corner cutting or refinement algorithms specified to generate a curve from a set of control
        points, or control polygon.
        :param points:                  the points of the polygon
        :param number_of_refinements:   the number of iterations to do, each iteration makes the polygon more smooth
        :return:                        a smoothed version of the input polygon
        """
        for _ in range(0, number_of_refinements):
            points_next_iter = []
            for num, pt in enumerate(points):
                P1, P2 = (pt, points[(num + 1) % len(points)])
                Q = BlobFactory._q_point(P1, P2)
                R = BlobFactory._r_point(P1, P2)
                points_next_iter.append(Q)
                points_next_iter.append(R)

            # get everything ready for next iteration
            points = points_next_iter

        # return
        return points
