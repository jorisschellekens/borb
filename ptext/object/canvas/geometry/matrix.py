class Matrix:
    def __init__(self):
        self.mtx = [[], [], []]

    @staticmethod
    def identity_matrix() -> "Matrix":
        m = Matrix()
        m.mtx = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        return m

    @staticmethod
    def matrix_from_six_values(
        a: float, b: float, c: float, d: float, e: float, f: float
    ):
        m = Matrix()
        m.mtx = [[a, b, 0], [c, d, 0], [e, f, 1]]
        return m

    def mul(self, y: "Matrix") -> "Matrix":
        m_vals = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    m_vals[i][j] += self.mtx[i][k] * y.mtx[k][j]
        m = Matrix()
        m.mtx = m_vals
        return m

    def cross(self, x: float, y: float, z: float):
        x2 = x * self[0][0] + y * self[1][0] + z * self[2][0]
        y2 = x * self[0][1] + y * self[1][1] + z * self[2][1]
        z2 = x * self[0][2] + y * self[1][2] + z * self[2][2]
        return x2, y2, z2

    def __getitem__(self, item):
        return self.mtx[item]

    def __str__(self):
        return "[[%f %f %f]\n [%f %f %f]\n [%f %f %f]]" % (
            self.mtx[0][0],
            self.mtx[0][1],
            self.mtx[0][2],
            self.mtx[1][0],
            self.mtx[1][1],
            self.mtx[1][2],
            self.mtx[2][0],
            self.mtx[2][1],
            self.mtx[2][2],
        )

    def __deepcopy__(self, memodict={}):
        m = Matrix()
        m.mtx = [
            [self.mtx[0][0], self.mtx[0][1], self.mtx[0][2]],
            [self.mtx[1][0], self.mtx[1][1], self.mtx[1][2]],
            [self.mtx[2][0], self.mtx[2][1], self.mtx[2][2]],
        ]
        return m
