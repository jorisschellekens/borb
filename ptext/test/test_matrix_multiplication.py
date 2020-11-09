import unittest

from ptext.object.canvas.geometry.matrix import Matrix


class TestMatrixMultiplication(unittest.TestCase):
    def test_matrix_multiplication(self):

        m0 = Matrix.identity_matrix()
        m0.mtx[2][0] = 121
        m0.mtx[2][1] = 613
        print(m0)
        print()

        m1 = Matrix.identity_matrix()
        m1.mtx[2][0] = -7
        m1.mtx[2][1] = -10
        print(m1)
        print()

        m2 = m0.mul(m1)
        print(m2)
        print()

        # asserts
        self.assertEqual(m2.mtx[0][0], 1)
        self.assertEqual(m2.mtx[0][1], 0)
        self.assertEqual(m2.mtx[0][2], 0)

        self.assertEqual(m2.mtx[1][0], 0)
        self.assertEqual(m2.mtx[1][1], 1)
        self.assertEqual(m2.mtx[1][2], 0)

        self.assertEqual(m2.mtx[2][0], 114)
        self.assertEqual(m2.mtx[2][1], 603)
        self.assertEqual(m2.mtx[2][2], 1)
