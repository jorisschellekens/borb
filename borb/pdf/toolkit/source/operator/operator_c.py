#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The 'C' operator: Append a cubic Bézier curve to the current path.

The 'C' operator is used to append a cubic Bézier curve to the current path in a PDF content stream.
The curve is defined by three points: the current point (which serves as the starting point),
the two control points (x1, y1) and (x2, y2), and the endpoint (x3, y3). The curve is drawn from
the current point to the point (x3, y3), using the control points to shape the curve.

After this operator is executed, the current point is updated to the endpoint (x3, y3).

Note:
    Refer to PDF specification section 8.5.2.2, "Cubic Bézier Curves", for more details on how
    Bézier curves are calculated and rendered.
"""
import typing

from borb.pdf.page import Page
from borb.pdf.primitives import PDFType
from borb.pdf.toolkit.source.operator.operator import Operator
from borb.pdf.toolkit.source.operator.source import (
    Source,
    ShapeType,
    LineType,
    PointType,
)


class Operatorc(Operator):
    """
    The 'C' operator: Append a cubic Bézier curve to the current path.

    The 'C' operator is used to append a cubic Bézier curve to the current path in a PDF content stream.
    The curve is defined by three points: the current point (which serves as the starting point),
    the two control points (x1, y1) and (x2, y2), and the endpoint (x3, y3). The curve is drawn from
    the current point to the point (x3, y3), using the control points to shape the curve.

    After this operator is executed, the current point is updated to the endpoint (x3, y3).

    Note:
        Refer to PDF specification section 8.5.2.2, "Cubic Bézier Curves", for more details on how
        Bézier curves are calculated and rendered.
    """

    #
    # CONSTRUCTOR
    #

    #
    # PRIVATE
    #

    @staticmethod
    def __bezier(
        p0: PointType, p1: PointType, p2: PointType, p3: PointType
    ) -> typing.List[LineType]:
        points: typing.List[PointType] = []
        for t in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
            x = (
                (1.0 - t) ** 3 * p0[0]
                + 3 * t * (1.0 - t) ** 2 * p1[0]
                + 3 * t**2 * (1.0 - t) * p2[0]
                + t**3 * p3[0]
            )
            y = (
                (1.0 - t) ** 3 * p0[1]
                + 3 * t * (1.0 - t) ** 2 * p1[1]
                + 3 * t**2 * (1.0 - t) * p2[1]
                + t**3 * p3[1]
            )
            points.append((x, y))

        # convert points to line_segments
        line_segments: typing.List[LineType] = []
        for i in range(1, len(points)):
            line_segments += [(points[i - 1], points[i])]

        # return
        return line_segments

    #
    # PUBLIC
    #

    def apply(
        self,
        operands: typing.List[PDFType],
        page: Page,
        source: Source,
    ) -> None:
        """
        Apply the operator's logic to the given `Page`.

        This method executes the operator using the provided operands, applying its
        effects to the specified `Page` via the `Source` processor. Subclasses should
        override this method to implement specific operator behavior.

        :param page: The `Page` object to which the operator is applied.
        :param source: The `Source` object managing the content stream.
        :param operands: A list of `PDFType` objects representing the operator's operands.
        """
        assert isinstance(operands[0], float) or isinstance(operands[0], int)
        assert isinstance(operands[1], float) or isinstance(operands[1], int)
        assert isinstance(operands[2], float) or isinstance(operands[2], int)
        assert isinstance(operands[3], float) or isinstance(operands[3], int)
        assert isinstance(operands[4], float) or isinstance(operands[4], int)
        assert isinstance(operands[5], float) or isinstance(operands[5], int)
        x1: typing.Union[float, int] = operands[0]
        y1: typing.Union[float, int] = operands[1]
        x2: typing.Union[float, int] = operands[2]
        y2: typing.Union[float, int] = operands[3]
        x3: typing.Union[float, int] = operands[4]
        y3: typing.Union[float, int] = operands[5]
        last_shape: ShapeType = source.path[-1]
        last_line: LineType = last_shape[-1]
        last_point: PointType = last_line[-1]
        source.path[-1].extend(
            Operatorc.__bezier(p0=last_point, p1=(x1, y1), p2=(x2, y2), p3=(x3, y3))
        )

    def get_name(self) -> str:
        """
        Retrieve the name of the operator.

        The name is a string identifier that corresponds to the operator
        in a PDF content stream (e.g., "BT" for Begin Text or "q" for Save Graphics State).

        :return: The name of the operator as a string.
        """
        return "c"

    def get_number_of_operands(self) -> int:
        """
        Retrieve the expected number of operands for this operator.

        The number of operands varies depending on the operator's purpose. For example,
        some operators might require no operands, while others may require multiple.

        :return: The number of operands expected by this operator as an integer.
        """
        return 6
