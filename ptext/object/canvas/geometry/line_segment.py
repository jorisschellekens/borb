from math import sqrt


class LineSegment:
    def __init__(self, x0: float, y0: float, x1: float, y1: float):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def length(self) -> float:
        return sqrt((self.x0 - self.x1) ** 2 + (self.y0 - self.y1) ** 2)

    def get_start(self) -> (float, float):
        return (self.x0, self.y0)

    def get_end(self) -> (float, float):
        return (self.x1, self.y1)

    def get_bounding_box(self) -> (float, float, float, float):
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
