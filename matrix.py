# @file matrix.py
# @author Evan Brody
# @brief Provides a Matrix class

import copy
from functools import reduce
from complex import Complex
import math

class Matrix:
    # p int number of rows
    # q int number of columns
    def __init__(self, vals: list = [[0]]) -> None:
        if len(vals) < 1:
            raise Exception("Error: must have a positive number of rows.")
        if len(vals[0]) < 1:
            raise Exception("Error: must have a positive number of columns.")

        q = len(vals[0])

        if not reduce(lambda a,b: a and len(b) == q, [True] + vals):
            raise Exception("Error: inconsistent number of columns.")

        self.p = len(vals)
        self.q = q
        self.vals = vals

    def __getitem__(self, i):
        return self.vals[i]

    def __setitem__(self, i, new_val):
        self.vals[i] = new_val

    @staticmethod
    def zeros(p: int, q: int = None):
        if q is None:
            q = p
        if p < 1 or q < 1:
            raise Exception("Error: matrix must have positive dimensions.")

        vals = [[0] * q]
        # This for loop is necessary because if you simply use another * n,
        # every element of the matrix will become a shallow copy of each other for some reason.
        for _ in range(p - 1):
            vals.append(copy.deepcopy(vals[0]))
        
        return Matrix(vals)

    @staticmethod
    def identity(n: int):
        if n < 1:
            raise Exception("Error: matrix must have positive dimensions.")

        res = Matrix.zeros(n)
        for i in range(n):
            res[i][i] = 1
        
        return res
    
    def trace(self) -> float:
        if self.p != self.q:
            raise Exception("Error: trace is undefined on a non-square matrix.")

        return sum([ self[i][i] for i in range(self.p) ])
    
    def is_square(self) -> bool:
        return self.p == self.q

    def is_invertible(self) -> bool:
        if self.p != self.q:
            raise Exception("Error: invertibility only defined for square matrices.")

        return abs(self.det()) >= 0.001

    def transpose(self):
        return Matrix([ [ self[i][j] for i in range(self.p) ] for j in range(self.q) ])

    def copy(self):
        return Matrix([ [ e for e in r ] for r in self.vals ])

    def inverse(self):
        if not self.is_invertible():
            raise Exception("Error: this matrix is not invertible.")

        mcopy = self.copy()
        res = Matrix.identity(self.p)
        vals = mcopy.vals
        for i, row in enumerate(vals):
            div = row[i]
            for j in range(len(row)):
                row[j] /= div
                res[i][j] /= div

            for i2 in range(len(vals)):
                if i == i2:
                    continue

                sub_mul = vals[i2][i]
                for j in range(len(vals[i2])):
                    vals[i2][j] -= vals[i][j] * sub_mul
                    res[i2][j] -= res[i][j] * sub_mul

        return res

    def det(self) -> float:
        if self.p != self.q:
            raise Exception("Error: determinant undefined for non-square matrices.")

        if self.p == 2 and self.q == 2:
            return self.vals[0][0] * self.vals[1][1] - self.vals[0][1] * self.vals[1][0]

        res = 0
        sign = 1
        for i, e in enumerate(self.vals[0]):
            sub_res = sign * e

            sub_vals = self.vals[1:]
            for j in range(len(sub_vals)):
                sub_vals[j] = sub_vals[j][:i] + sub_vals[j][i + 1:]
            sub_res *= Matrix(sub_vals).det()

            res += sub_res
            sign = -sign

        return res

    def __neg__(self):
        return Matrix([ [ -e for e in r ] for r in self.vals ])

    def __add__(self, rhs):
        if self.p != rhs.p or self.q != rhs.q:
            raise Exception("Error: attempting to add matrices with different dimensions.")

        return Matrix([ [ self[i][j] + rhs[i][j] for j in range(self.q) ] for i in range(self.p) ])

    def __sub__(self, rhs):
        return self + (-rhs)

    def __mul__(self, rhs):
        if isinstance(rhs, int) or isinstance(rhs, float):
            return Matrix([ [ self[i][j] * rhs for j in range(self.q) ] for i in range(self.p) ])

        if self.q != rhs.p:
            raise Exception("Error: incompatible dimensions for dot product.")
            return

        return Matrix([ [ sum([ self[i][k] * rhs[k][j] for k in range(self.q) ]) for j in range(rhs.q) ] for i in range(self.p) ])
    
    def __rmul__(self, lhs):
        if not (isinstance(lhs, int) or isinstance(lhs, float)):
            raise Exception("Error: must only multiply by a matrix or a scalar.")
        
        res = []
        for row in self.vals:
            new_row = list(map(lambda x: lhs*x, row))
            res.append(new_row)

        return Matrix(res)
    
    def __pow__(self, n):
        if self.p != self.q:
            raise Exception("Error: can only exponentiate a square matrix.")
        if 0 == n:
            return Matrix.identity(self.p)
        
        base = self
        
        if n > 0:
            res = Matrix(copy.deepcopy(self.vals))
        else:
            base = self.inverse()
            res = self.inverse()
            n = abs(n)
        
        log2n = math.floor(math.log(n, 2))
        for _ in range(log2n):
            res *= res
        
        for _ in range(n - (2 ** log2n)):
            res *= base

        return res

    def __eq__(self, rhs) -> bool:
        if not isinstance(rhs, Matrix):
            raise Exception("Error: equality check is only defined for other matrices.")

        if self.p != rhs.p or self.q != rhs.q:
            return False
        
        return all([ all([ self[i][j] == rhs[i][j] for j in range(self.q) ]) for i in range(self.p) ])

    def __repr__(self) -> str:
        col_lengths = [max(len(str(self[i][j])) for i in range(self.p)) for j in range(self.q)]

        res = ""
        for i in range(self.p):
            srow = "[ "
            for j in range(self.q):
                srow += f"{str(self[i][j]):>{col_lengths[j]}} "
            srow += "]\n"
            res += srow

        return res

def test():
    m1 = Matrix([[1, 1],
                [2, 2]])
    m2 = Matrix([[3, 3],
                [4, 4]])
    m3 = m1 + m2
    print(m3)

    m1 = Matrix([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])
    m2 = Matrix([[10, 11, 12],
                 [13, 14, 15],
                 [16, 17, 18]])
    m3 = m1 * m2
    print(m3)
    # [ 84 90 96 ]
    # [ 201 216 231 ]
    # [ 318 342 366 ]

    m1 = Matrix([[1, 2, 3],
                 [4, 5, 6]])
    m2 = Matrix([[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12]])
    m3 = m1 * m2
    print(m3)
    # [ 38 44 50 56 ]
    # [ 83 98 113 128 ]


    print(-1 * m1)
    print(m1 * -1)
    print(-1 * m1 * m2)
    print(m1 * m2 * -1)
    print(m1 == m1)
    print(m1 == 2 * m1)
    print()

    m1 = Matrix([[1, 2],
                 [0, 1]])
    m2 = Matrix([[0, 0],
                 [0, 0]])
    print(m1.is_invertible())
    print(m2.is_invertible())

    print("transpose")
    m2 = Matrix([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])
    print(m2.transpose())

    m1 = Matrix([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]])
    m2 = m1 ** 3

    print(m1)
    print(m2)

    m1.vals[0][2] = 7
    print(m1)
    print(m2)

    m1 = Matrix([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])
    print(m1 ** 3)

    print(Matrix.identity(3))
    print(3 * Matrix.identity(3))
    print(Matrix.zeros(4))

    # Invalid; inconsistent num of columns
    # m1 = Matrix([[1, 2, 3],
    #              [4, 5],
    #              [7, 8, 9]])

    m1 = Matrix()

    m2 = Matrix.identity(3)
    print(m2.trace())

    m1 = Matrix([[Complex(0, 1), Complex(), Complex()],
                 [Complex(), Complex(0, 1), Complex()],
                 [Complex(), Complex(), Complex(0, 1)]])
    m2 = Matrix([[Complex(0, 1), Complex(), Complex()],
                [Complex(), Complex(0, 1), Complex()],
                [Complex(), Complex(), Complex(0, 1)]])
    print()
    print(m1 * m2)

    m1 = Matrix([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]])

    print(m1.det())
    print()

    m1 = Matrix([[Complex(1, 1), Complex(2, 1), Complex(3, 1), Complex(4, 1)],
                [Complex(5, 1), Complex(6, 1), Complex(7, 1), Complex(8, 1)],
                [Complex(9, 1), Complex(-1, 1), Complex(-2, 1), Complex(-3, 1)],
                 [Complex(-4, 1), Complex(-5, 1), Complex(-6, 1), Complex(-7, 1)]])
    print(m1.det())

    m = Matrix([[Complex(2, 1), Complex(3)],
                [Complex(2), Complex(2)]])
    print(m.inverse())
    print(m * m.inverse())

    m = Matrix([[2, 0, 0],
                [0, 2, 0],
                [0, 0, 2]])
    print(m ** 9)
    print(m ** -2)

if __name__ == "__main__":
    test()