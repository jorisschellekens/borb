import unittest
from decimal import Decimal

from borb.pdf.canvas.geometry.matrix import Matrix


class TestMatrixMultiplication(unittest.TestCase):
    def test_matrix_multiplication(self):

        m0 = Matrix.identity_matrix()
        m0.mtx[2][0] = Decimal(121)
        m0.mtx[2][1] = Decimal(613)
        print(m0)
        print()

        m1 = Matrix.identity_matrix()
        m1.mtx[2][0] = Decimal(-7)
        m1.mtx[2][1] = Decimal(-10)
        print(m1)
        print()

        m2 = m0.mul(m1)
        print(m2)
        print()

        # asserts
        self.assertEqual(m2.mtx[0][0], Decimal(1))
        self.assertEqual(m2.mtx[0][1], Decimal(0))
        self.assertEqual(m2.mtx[0][2], Decimal(0))

        self.assertEqual(m2.mtx[1][0], Decimal(0))
        self.assertEqual(m2.mtx[1][1], Decimal(1))
        self.assertEqual(m2.mtx[1][2], Decimal(0))

        self.assertEqual(m2.mtx[2][0], Decimal(114))
        self.assertEqual(m2.mtx[2][1], Decimal(603))
        self.assertEqual(m2.mtx[2][2], Decimal(1))
