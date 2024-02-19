class PolynomialCalculator:
    def input(self):
        print("Enter coefficients of first polynomial separated by spaces:")
        coeffs1 = list(map(int, input().split()))
        self.poly1_matrix = Matrix([[Polynomial(coeffs1)]])

        print("Enter coefficients of second polynomial separated by spaces:")
        coeffs2 = list(map(int, input().split()))
        self.poly2_matrix = Matrix([[Polynomial(coeffs2)]])

    def display(self):
        print("First Polynomial:")
        print(self.poly1_matrix)
        print("Second Polynomial:")
        print(self.poly2_matrix)

    def add(self):
        self.poly_sum = self.poly1_matrix + self.poly2_matrix
        print("Sum of Polynomials:")
        print(self.poly_sum)

    def subtract(self):
        self.poly_diff = self.poly1_matrix - self.poly2_matrix
        print("Difference of Polynomials:")
        print(self.poly_diff)

    def multiply(self):
        self.poly_product = self.poly1_matrix * self.poly2_matrix
        print("Product of Polynomials:")
        print(self.poly_product)

    def read_data(self, path):
        with open(path, 'r') as file:
            coeffs1 = list(map(int, file.readline().split()))
            coeffs2 = list(map(int, file.readline().split()))
        
        self.poly1_matrix = Matrix([[Polynomial(coeffs1)]])
        self.poly2_matrix = Matrix([[Polynomial(coeffs2)]])

    def write_data(self, path):
        with open(path, 'w') as file:
            file.write("First Polynomial:\n")
            file.write(str(self.poly1_matrix) + "\n")
            file.write("Second Polynomial:\n")
            file.write(str(self.poly2_matrix) + "\n")
            file.write("Sum of Polynomials:\n")
            file.write(str(self.poly_sum) + "\n")
            file.write("Difference of Polynomials:\n")
            file.write(str(self.poly_diff) + "\n")
            file.write("Product of Polynomials:\n")
            file.write(str(self.poly_product) + "\n")
