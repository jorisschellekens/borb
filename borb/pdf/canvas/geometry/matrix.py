#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
In mathematics, a matrix (plural matrices) is a rectangular array or table of numbers,
symbols, or expressions, arranged in rows and columns.
"""
import typing
from decimal import Decimal


class Matrix:
    """
    In mathematics, a matrix (plural matrices) is a rectangular array or table of numbers, symbols, or expressions, arranged in rows and columns.
    Provided that they have the same size (each matrix has the same number of rows and the same number of columns as the other),
    two matrices can be added or subtracted element by element (see conformable matrix).

    The rule for matrix multiplication, however, is that two matrices can be multiplied only when the number of columns
    in the first equals the number of rows in the second (i.e., the inner dimensions are the same, n for an (m×n)-matrix times an (n×p)-matrix,
    resulting in an (m×p)-matrix). There is no product the other way round—a first hint that matrix multiplication is not commutative.
    Any matrix can be multiplied element-wise by a scalar from its associated field.
    """

    #
    # CONSTRUCTOR
    #

    def __init__(self):
        """
        Initialize a new Matrix
        """
        self.mtx: typing.List[typing.List[Decimal]] = [[], [], []]

    #
    # PRIVATE
    #

    def __deepcopy__(self, memodict={}):
        m = Matrix()
        m.mtx = [
            [self.mtx[0][0], self.mtx[0][1], self.mtx[0][2]],
            [self.mtx[1][0], self.mtx[1][1], self.mtx[1][2]],
            [self.mtx[2][0], self.mtx[2][1], self.mtx[2][2]],
        ]
        return m

    def __getitem__(self, item) -> typing.List[Decimal]:
        return self.mtx[item]

    def __str__(self):
        return "[[%f %f %f]\n [%f %f %f]\n [%f %f %f]]" % (
            float(self.mtx[0][0]),
            float(self.mtx[0][1]),
            float(self.mtx[0][2]),
            float(self.mtx[1][0]),
            float(self.mtx[1][1]),
            float(self.mtx[1][2]),
            float(self.mtx[2][0]),
            float(self.mtx[2][1]),
            float(self.mtx[2][2]),
        )

    #
    # PUBLIC
    #

    def cross(
        self, x: Decimal, y: Decimal, z: Decimal
    ) -> typing.Tuple[Decimal, Decimal, Decimal]:
        """
        This method calculates the dot-product of this Matrix
        with an input vector (represented by 3 input Decimal objects)
        and returns the result
        :param x:   the first component of the vector
        :param y:   the second component of the vector
        :param z:   the third component of the vector
        :return:    the result vector
        """
        x2 = x * self[0][0] + y * self[1][0] + z * self[2][0]
        y2 = x * self[0][1] + y * self[1][1] + z * self[2][1]
        z2 = x * self[0][2] + y * self[1][2] + z * self[2][2]
        return x2, y2, z2

    def determinant(self) -> Decimal:
        """
        In linear algebra, the determinant is a scalar value that can be computed from the elements of a square matrix
        and encodes certain properties of the linear transformation described by the matrix.
        The determinant of a matrix A is denoted det(A), det A, or |A|.
        Geometrically, it can be viewed as the volume scaling factor of the linear transformation described by the matrix.
        This is also the signed volume of the n-dimensional parallelepiped spanned by the column or row vectors of the matrix.
        The determinant is positive or negative according to whether the linear transformation preserves or reverses the orientation of a real vector space.
        :return:    the determinant of this Matrix
        """
        return (
            self.mtx[0][0]
            * (self.mtx[1][1] * self.mtx[2][2] - self.mtx[1][2] * self.mtx[2][1])
            - self.mtx[0][1]
            * (self.mtx[1][0] * self.mtx[2][2] - self.mtx[1][2] * self.mtx[2][0])
            + self.mtx[0][2]
            * (self.mtx[1][0] * self.mtx[2][1] - self.mtx[1][1] * self.mtx[2][0])
        )

    @staticmethod
    def identity_matrix() -> "Matrix":
        """
        The identity matrix In of size n is the n-by-n matrix in which all the elements on the main diagonal
        are equal to 1 and all other elements are equal to 0.
        :return:    the identity Matrix
        """
        m = Matrix()
        m.mtx = [
            [Decimal(1), Decimal(0), Decimal(0)],
            [Decimal(0), Decimal(1), Decimal(0)],
            [Decimal(0), Decimal(0), Decimal(1)],
        ]
        return m

    @staticmethod
    def matrix_from_six_values(
        a: Decimal, b: Decimal, c: Decimal, d: Decimal, e: Decimal, f: Decimal
    ):
        """
        This method returns the matrix [[a, b, 0], [c, d, 0], [e, f, 1]]
        :param a:   the component at (0, 0)
        :param b:   the component at (0, 1)
        :param c:   the component at (1, 0)
        :param d:   the component at (1, 1)
        :param e:   the component at (2, 0)
        :param f:   the component at (2, 1)
        :return:    the Matrix
        """
        m = Matrix()
        m.mtx = [[a, b, Decimal(0)], [c, d, Decimal(0)], [e, f, Decimal(1)]]
        return m

    def mul(self, y: "Matrix") -> "Matrix":
        """
        This function multiplies this Matrix with another Matrix, returning the result
        :param y:   the Matrix to multiply by
        :return:    the resulting Matrix
        """
        m_vals = [
            [Decimal(0), Decimal(0), Decimal(0)],
            [Decimal(0), Decimal(0), Decimal(0)],
            [Decimal(0), Decimal(0), Decimal(0)],
        ]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    m_vals[i][j] += self.mtx[i][k] * y.mtx[k][j]
        m = Matrix()
        m.mtx = m_vals
        return m
