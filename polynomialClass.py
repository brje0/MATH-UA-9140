class Term:
    def __init__(self, coefficient, exponent):
        self.coefficient = coefficient
        self.exponent = exponent

class Polynomial:
    def __init__(self):
        self.terms = []

    def add_term(self, coefficient, exponent):
        self.terms.append(Term(coefficient, exponent))

    def evaluate(self, x):
        result = 0
        for term in self.terms:
            result += term.coefficient * (x ** term.exponent)
        return result

    def __str__(self):
        terms_str = []
        for term in self.terms:
            if term.exponent == 0:
                terms_str.append(str(term.coefficient))
            elif term.exponent == 1:
                terms_str.append(f"{term.coefficient}x")
            else:
                terms_str.append(f"{term.coefficient}x^{term.exponent}")
        return " + ".join(terms_str)

class PolyMatrix:
    def __init__(self, rows, cols):
        self.matrix = [[Polynomial() for _ in range(cols)] for _ in range(rows)]

    def set_element(self, row, col, polynomial):
        if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[0]):
            self.matrix[row][col] = polynomial

    def get_element(self, row, col):
        if 0 <= row < len(self.matrix) and 0 <= col < len(self.matrix[0]):
            return self.matrix[row][col]
        else:
            return Polynomial()

# Example usage
poly_matrix = PolyMatrix(1, 2)

poly1 = Polynomial()
poly1.add_term(3, 2)  # 3x^2
poly1.add_term(2, 1)  # 2x
poly1.add_term(1, 0)  # 1
poly_matrix.set_element(0, 0, poly1)

poly2 = Polynomial()
poly2.add_term(1, 1)  # x
poly2.add_term(2, 0)  # 2
poly_matrix.set_element(0, 1, poly2)

poly3 = poly_matrix.get_element(0, 0)
print("Element at (0, 0):", poly3)
