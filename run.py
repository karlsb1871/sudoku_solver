import numpy as np
import pandas as pd
from scipy.optimize import milp, Bounds, LinearConstraint


def read_sudoku_from_csv(path: str):
    df = pd.read_csv(path, sep=",", header=None)
    return df


def generate_objective():
    return np.array([0 for i in range(9) for j in range(9) for k in range(9)])


def generate_bounds():
    return Bounds(
        [0 for i in range(9) for j in range(9) for k in range(9)],
        [1 for i in range(9) for j in range(9) for k in range(9)],
    )


def generate_appear_once_per_row_constraints():
    A = []
    b_u = []
    b_l = []
    for i in range(9):
        for k in range(9):
            A.append(
                [
                    1 if ii == i and kk == k else 0
                    for ii in range(9)
                    for jj in range(9)
                    for kk in range(9)
                ]
            )
            b_u.append(1)
            b_l.append(1)

    return A, b_l, b_u


def generate_appear_once_per_col_constraints():
    A = []
    b_u = []
    b_l = []
    for j in range(9):
        for k in range(9):
            A.append(
                [
                    1 if jj == j and kk == k else 0
                    for ii in range(9)
                    for jj in range(9)
                    for kk in range(9)
                ]
            )
            b_u.append(1)
            b_l.append(1)

    return A, b_l, b_u


def generate_appear_once_per_square_constraints():
    A = []
    b_u = []
    b_l = []
    for i in range(3):
        for j in range(3):
            for k in range(9):
                A.append(
                    [
                        1 if int(ii / 3) == i and int(jj / 3) == j and kk == k else 0
                        for ii in range(9)
                        for jj in range(9)
                        for kk in range(9)
                    ]
                )
                b_u.append(1)
                b_l.append(1)

    return A, b_l, b_u


def generate_one_number_per_cell_constraints():
    A = []
    b_u = []
    b_l = []
    for i in range(9):
        for j in range(9):
            A.append(
                [
                    1 if ii == i and jj == j else 0
                    for ii in range(9)
                    for jj in range(9)
                    for kk in range(9)
                ]
            )
            b_u.append(1)
            b_l.append(1)

    return A, b_l, b_u


def generate_current_values_constraints(sudoku: pd.DataFrame):
    A = []
    b_l = []
    b_u = []
    for i in range(9):
        for j in range(9):
            if sudoku.iloc[i, j] != 0:
                value = sudoku.iloc[i, j] - 1
                A.append(
                    [
                        1 if ii == i and jj == j and kk == value else 0
                        for ii in range(9)
                        for jj in range(9)
                        for kk in range(9)
                    ]
                )
                b_u.append(1)
                b_l.append(1)

    return A, b_l, b_u


def main():
    sudoku = read_sudoku_from_csv("test_sudokus/arto_inkala.csv")

    c = generate_objective()
    A = []
    b_l = []
    b_u = []
    constraints = [
        generate_appear_once_per_row_constraints,
        generate_appear_once_per_col_constraints,
        generate_appear_once_per_square_constraints,
        generate_one_number_per_cell_constraints,
        lambda: generate_current_values_constraints(sudoku),
    ]
    for constraint in constraints:
        con = constraint()
        A.extend(con[0])
        b_l.extend(con[1])
        b_u.extend(con[1])

    bnds = generate_bounds()

    res = milp(
        c=c,
        constraints=LinearConstraint(A, b_l, b_u),
        bounds=bnds,
        integrality=np.ones_like(c),
    )

    for i in range(9):
        row = []
        for j in range(9):
            for k in range(9):
                if res.x[81 * i + 9 * j + k] >= 0.5:
                    row.append(k + 1)
        print(row)


if __name__ == "__main__":
    main()
