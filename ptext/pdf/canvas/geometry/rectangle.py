from decimal import Decimal


class Rectangle:
    """
    In Euclidean plane geometry, a rectangle is a quadrilateral with four right angles.
    It can also be defined as an equiangular quadrilateral, since equiangular means that all of its angles are equal (360°/4 = 90°).
    It can also be defined as a parallelogram containing a right angle. A rectangle with four sides of equal length is a square.
    The term oblong is occasionally used to refer to a non-square rectangle.
    """

    def __init__(self, x: Decimal, y: Decimal, width: Decimal, height: Decimal):
        assert width >= 0
        assert height >= 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_x(self) -> Decimal:
        return self.x

    def get_y(self) -> Decimal:
        return self.y

    def get_width(self) -> Decimal:
        return self.width

    def get_height(self) -> Decimal:
        return self.height
