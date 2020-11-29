from decimal import Decimal
from math import sqrt


class LineSegment:
    def __init__(self, x0: Decimal, y0: Decimal, x1: Decimal, y1: Decimal):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def length(self) -> Decimal:
        return Decimal(sqrt((self.x0 - self.x1) ** 2 + (self.y0 - self.y1) ** 2))

    def get_start(self) -> (Decimal, Decimal):
        return (self.x0, self.y0)

    def get_end(self) -> (Decimal, Decimal):
        return (self.x1, self.y1)

    def get_bounding_box(self) -> (Decimal, Decimal, Decimal, Decimal):
        """
        return the bounding box of this rectangle in the format
        (lower_left_x, lower_left_y, width, height)
        """
        return (
            min(self.x0, self.x1),
            min(self.y0, self.y1),
            abs(self.x0 - self.x1),
            abs(self.y0 - self.y1),
        )

    def transform_by(self, matrix: "Matrix") -> "LineSegment":
        p0 = matrix.cross(self.x0, self.y0, 1)
        p1 = matrix.cross(self.x1, self.y1, 1)
        return LineSegment(p0[0], p0[1], p1[0], p1[1])
