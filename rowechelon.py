from matrix import Matrix
import copy

def row_echelon(matrix):
    # Make a copy of the original matrix to avoid modifying it
    mat = copy.deepcopy(matrix)

    rows, cols = mat.p, mat.q

    lead = 0
    for r in range(rows):
        if lead >= cols:
            break

        # Find the first nonzero entry in the column 'lead' from row 'r'
        i = r
        while mat[i][lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if cols == lead:
                    return mat  # Return if all columns are done

        # Swap the rows
        mat[i], mat[r] = mat[r], mat[i]

        # Scale the current row to make the leading entry 1
        lv = mat[r][lead]
        mat[r] = [x / lv for x in mat[r]]

        # Eliminate the leading entry from all other rows
        for i in range(rows):
            if i != r:
                lv = mat[i][lead]
                mat[i] = [mat[i][j] - lv * mat[r][j] for j in range(cols)]

        lead += 1

    return mat

# Example usage:
if __name__ == "__main__":
    # Create a matrix
    m = Matrix([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

    print("Original matrix:")
    print(m)

    # Apply row echelon transformation
    echelon_matrix = row_echelon(m)

    print("\nMatrix after row echelon transformation:")
    print(echelon_matrix)
