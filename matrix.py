# @file matrix.py
# @author Evan Brody
# @brief Provides a Matrix class
import copy
from functools import reduce

class Matrix:
    # p int number of rows
    # q int number of columns
    def __init__(self, vals: list = [[0]]) -> None:
        if len(vals) < 1:
            print("Error: must have a positive number of rows.")
            return
        if len(vals[0]) < 1:
            print("Error: must have a positive number of columns.")
            return

        q = len(vals[0])

        if not reduce(lambda a,b: a and len(b) == q, [True] + vals):
            print("Error: inconsistent number of columns.")
            return

        self.p = len(vals)
        self.q = q
        self.vals = vals

    def __getitem__(self, i):
        return self.vals[i]

    @staticmethod
    def zeros(p: int, q: int = None):
        if q is None:
            q = p
        if p < 1 or q < 1:
            print("Error: matrix must have positive dimensions.")
            return
        vals = [[0] * q]
        # This for loop is necessary because if you simply use another * n,
        # every element of the matrix will become a shallow copy of each other for some reason.
        for _ in range(p - 1):
            vals.append(copy.deepcopy(vals[0]))
        
        return Matrix(vals)

    @staticmethod
    def identity(n: int):
        if n < 1:
            print("Error: matrix must have positive dimensions.")
            return
        res = Matrix.zeros(n)
        for i in range(n):
            res[i][i] = 1
        
        return res
    
    def trace(self) -> float:
        if self.p != self.q:
            print("Error: trace is undefined on a non-square matrix.")
            return
        
        res = 0
        for i in range(self.p):
            res += self[i][i]
        
        return res
    
    def is_square(self) -> bool:
        return self.p == self.q

    def is_invertible(self) -> bool:
        if self.p != 2 or self.q != 2:
            print("Error: is_invertible() only defined for 2x2 matrices.")
            return

        return 0 != self.vals[0][0] * self.vals[1][1] - self.vals[0][1] * self.vals[1][0]

    def transpose(self):
        res = []
        for j in range(self.q):
            res.append([self.vals[i][j] for i in range(self.p)])

        return Matrix(res)

    def __add__(self, rhs):
        if self.p != rhs.p or self.q != rhs.q:
            print("Attempting to add matrices with different dimensions.")
            return

        res = [ [ self[i][j] + rhs[i][j] for j in range(self.q) ] for i in range(self.p) ]

        return Matrix(res)
    
    def __mul__(self, rhs):
        if isinstance(rhs, int) or isinstance(rhs, float):
            res = []
            for row in self.vals:
                new_row = list(map(lambda x: x*rhs, row))
                res.append(new_row)
            
            return Matrix(res)

        if self.q != rhs.p:
            print("Error: incompatible dimensions for dot product.")
            return

        res = Matrix.zeros(self.p, rhs.q)
        for i in range(self.p):
            for j in range(self.q):
                res[i][j] = sum([ self[i][k] * rhs[k][j] for k in range(self.q) ])
        
        return res
    
    def __rmul__(self, lhs):
        if not (isinstance(lhs, int) or isinstance(lhs, float)):
            print("Error: must only multiply by a matrix or a scalar.")
            return
        
        res = []
        for row in self.vals:
            new_row = list(map(lambda x: lhs*x, row))
            res.append(new_row)

        return Matrix(res)
    
    def __pow__(self, exp):
        if self.p != self.q:
            print("Error: can only exponentiate a square matrix.")
            return
        if 0 == exp:
            return Matrix.identity(self.p)
        
        res = Matrix(copy.deepcopy(self.vals))
        for _ in range(exp - 1):
            res *= self

        return res

    def __eq__(self, rhs) -> bool:
        if not isinstance(rhs, Matrix):
            print("Error: equality check is only defined for other matrices.")
            return
        
        if self.p != rhs.p or self.q != rhs.q:
            return False
        
        return all([ all([ self[i][j] == rhs[i][j] for j in range(self.q) ]) for i in range(self.p)])

    def __repr__(self) -> str:
        res = ""
        for row in self.vals:
            srow = "[ "
            for elem in row:
                srow += str(elem) + ' '
            srow += "]\n"
            res += srow
        
        return res

def main():
    # Testing code
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

    m1 = Matrix([[1, 2, 3],
                 [4, 5, 6]])
    m2 = Matrix([[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12]])
    m3 = m1 * m2
    print(m3)

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

    m1 = Matrix([[1, 2, 3],
                 [4, 5],
                 [7, 8, 9]])
main()