# @file main.py
# @author Evan Brody
# @brief Provides user input handling to interact with Matrix class functions.

from matrix import Matrix
from complex import Complex
import os

def str_to_complex(s: str):
    s = s.replace(' ', '')
    iloc = s.find('i')
    if iloc == -1:
        return Complex(float(s), 0)
    else:
        # Finding complex component
        c = ''
        i = iloc + 1
        while i < len(s) and s[i] not in "+-":
            c += s[i]
            i += 1
        if c == '':
            i = iloc - 1
            while i > -1 and s[i] not in "+-":
                c = s[i] + c
                i -= 1
        if c == '':
            cfloat = 1
        else:
            cfloat = float(c)
        i = iloc - 1
        while i > -1:
            if s[i] == '-':
                cfloat = -cfloat
                break
            i -= 1

        # Finding real component
        left = iloc
        right = iloc
        while left >= 0 and s[left] not in "+-":
            left -= 1
        left += 1
        while right < len(s) and s[right] not in "+-":
            right += 1
        s = s.replace(s[left:right], '')
        s = s.replace('+', '')
        if s != '':
            if s[0] == '-':
                neg = True
            else:
                neg = False
            s = s.replace('-', '')
            if s != '':
                rfloat = float(s)
            else:
                rfloat = 0
            if neg:
                rfloat = -rfloat
        else:
            rfloat = 0

        return Complex(rfloat, cfloat)

def pretty_print(vals):
    if len(vals) == 0 or len(vals[0]) == 0:
        return
    col_lengths = [ max([ len(str(vals[i][j])) for i in range(len(vals)) ]) for j in range(len(vals[0])) ]

    res = ''
    for i in range(len(vals)):
        srow = ''
        for j in range(len(vals[i])):
            srow += f"{str(vals[i][j]):>{col_lengths[j]}} "
        res += srow + '\n'

    print(res[:-1], end='')

def get_matrix():
    p, q = get_dims()
    print("Enter your matrix:")
    vals = []
    for _ in range(p):
        vals.append([''] * q)

    for i in range(p):
        for j in range(q):
            os.system("cls" if os.name == "nt" else "clear")
            print("Enter your matrix:")
            pretty_print(vals)
            vals[i][j] = str_to_complex(input())

    return Matrix(vals)

def get_dims():
    p = int(input("How many rows ? "))
    q = int(input("How many columns ? "))
    return p, q

def main():
    print("""
        S: Sum
        P: Product
        E: Exponentiation
        T: Trace
        D: Determinant
        I: Inverse
          """)
    choice = input("Choose an operation: ").upper()

    m = get_matrix()

    match choice:
        case 'S':
            m2 = get_matrix()
            print("Sum:")
            print(m + m2)
        case 'P':
            m2 = get_matrix()
            print("Product:")
            print(m * m2)
        case 'E':
            n = int(input("Enter the power to raise this matrix to: "))
            print("Result:")
            print(m ** n)
        case 'T':
            print("Trace:")
            print(m.trace())
        case 'D':
            print("Determinant:")
            print(m.det())
        case 'I':
            print("Inverse:")
            print(m.inverse())
        case _:
            print("Invalid operation selected.")

if __name__ == "__main__":
    main()
