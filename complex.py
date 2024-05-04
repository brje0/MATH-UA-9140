# @file complex.py
# @author Evan Brody
# @brief Implements a basic class for dealing with complex numbers

class Complex:
    def __init__(self, r: float = 0, c: float = 0):
        self.r = r
        self.c = c

    def __abs__(self) -> float:
        return (self.r ** 2 + self.c ** 2) ** 0.5

    def __neg__(self):
        return Complex(-self.r, -self.c)

    def __add__(self, rhs):
        if isinstance(rhs, Complex):
            return Complex(self.r + rhs.r, self.c + rhs.c)
        else:
            return Complex(self.r + rhs, self.c)

    def __sub__(self, rhs):
        return self + (-rhs)

    def __rsub__(self, lhs):
        return lhs + (-self)

    def __radd__(self, lhs):
        return self + lhs

    def __mul__(self, rhs):
        if isinstance(rhs, Complex):
            return Complex(self.r * rhs.r - self.c * rhs.c, self.r * rhs.c + self.c * rhs.r)
        else:
            return Complex(self.r * rhs, self.c * rhs)

    def __rmul__(self, lhs):
        return self * lhs

    def __truediv__(self, rhs):
        if isinstance(rhs, Complex):
            den = rhs.r ** 2 + rhs.c ** 2
            r = (self.r * rhs.r + self.c * rhs.c) / den
            c = (self.c * rhs.r - self.r * rhs.c) / den
            return Complex(r, c)
        else:
            return Complex(self.r / rhs, self.c / rhs)

    def __rtruediv__(self, lhs):
        return Complex(lhs) / self

    def __str__(self):
        if self.r == 0 and self.c != 0:
            if self.c == 1:
                return 'i'
            elif self.c == -1:
                return '-i'
            else:
                return f"i{self.c}"
        elif self.c == 0:
            return str(self.r)
        elif self.c == 1:
            return f"{self.r} + i"
        elif self.c == -1:
            return f"{self.r} - i"
        elif self.c < 0:
            return f"{self.r} - i{-self.c}"
        else:
            return f"{self.r} + i{self.c}"