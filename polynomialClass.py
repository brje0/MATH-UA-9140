#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <cmath>

// Structure to represent a term in a polynomial expression
struct Term {
    int coefficient;
    int exponent;
};

// Class to represent a polynomial expression
class Polynomial {
private:
    std::vector<Term> terms;

public:
    // Method to add a term to the polynomial
    void addTerm(int coefficient, int exponent) {
        terms.push_back({coefficient, exponent});
    }

    // Method to evaluate the polynomial for a given value of x
    int evaluate(int x) const {
        int result = 0;
        for (const auto& term : terms) {
            result += term.coefficient * std::pow(x, term.exponent);
        }
        return result;
    }

    // Method to convert the polynomial to a string representation
    std::string toString() const {
        std::ostringstream oss;
        for (size_t i = 0; i < terms.size(); ++i) {
            const auto& term = terms[i];
            if (i != 0) {
                oss << " + ";
            }
            oss << term.coefficient;
            if (term.exponent != 0) {
                oss << "x";
                if (term.exponent != 1) {
                    oss << "^" << term.exponent;
                }
            }
        }
        return oss.str();
    }
};

// Class to represent a matrix of polynomial expressions
class PolyMatrix {
private:
    std::vector<std::vector<Polynomial>> matrix;

public:
    // Method to add a polynomial expression to the matrix at a specific row and column
    void setElement(int row, int col, const Polynomial& polynomial) {
        if (row >= 0 && row < matrix.size() && col >= 0 && col < matrix[0].size()) {
            matrix[row][col] = polynomial;
        }
    }

    // Method to retrieve a polynomial expression from the matrix at a specific row and column
    Polynomial getElement(int row, int col) const {
        if (row >= 0 && row < matrix.size() && col >= 0 && col < matrix[0].size()) {
            return matrix[row][col];
        } else {
            // Return an empty polynomial if indices are out of bounds
            return Polynomial();
        }
    }
};

int main() {
    // Example usage
    PolyMatrix polyMatrix;

    Polynomial poly1;
    poly1.addTerm(3, 2); // 3x^2
    poly1.addTerm(2, 1); // 2x
    poly1.addTerm(1, 0); // 1
    polyMatrix.setElement(0, 0, poly1);

    Polynomial poly2;
    poly2.addTerm(1, 1); // x
    poly2.addTerm(2, 0); // 2
    polyMatrix.setElement(0, 1, poly2);

    Polynomial poly3 = polyMatrix.getElement(0, 0);
    std::cout << "Element at (0, 0): " << poly3.toString() << std::endl;

    return 0;
}
