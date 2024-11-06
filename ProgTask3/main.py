from asyncio.windows_events import INFINITE
from sys import maxsize
import copy

def get_input():
    S = [int(x) for x in input("Enter coefficients of supply: ").split()]
    C = []
    for i in range(len(S)):
        C_row = [int(x) for x in input(f"Enter costs for {i+1}: ").split()]
        C.append(C_row)
    D = [int(x) for x in input("Enter coefficients of demand: ").split()]
    return S, C, D

def print_table(S, C, D):
    print("\n", end="\t")
    for i in range(len(C[0])):
        print(f"B{i+1}", end="\t")
    print("Supply")
    for i in range(len(C)):
        print(f"A{i+1}", end="\t")
        for j in range(len(C[0])):
            print(C[i][j], end="\t")
        print(S[i])
    print("Demand", end="\t")
    for j in range(len(D)):
        print(D[j], end="\t")
    print()

def check_applicability(S, C, D):
    if any(x < 0 for x in S) or any(x < 0 for x in D):
        return False
    for i in range(len(C)):
        if any(x < 0 for x in C[i]):
            return False
    return True

def eliminate_row(C, i, coeff):
    for j in range(len(C[i])):
        if coeff[i][j] == 0:
            C[i][j] = -1
    return C

def eliminate_column(C, j, coeff):
    for i in range(len(C)):
        if coeff[i][j] == 0:
            C[i][j] = -1
    return C

def find_vogels_penalty(C):
    row_penalty = []
    col_penalty = []

    # Calculating row penalties
    for i in range(len(C)):
        row_values = sorted([c for c in C[i]])
        row_penalty.append(row_values[1] - row_values[0])

    # Calculating column penalties
    for col in range(len(C[0])):
        col_values = sorted([C[i][col] for i in range(len(C))])
        col_penalty.append(col_values[1] - col_values[0])

    return row_penalty, col_penalty

def vogels_approximation(S, C, D):
    answer = 0
    while sum(S) > 0 or sum(D) > 0:
        row_penalty, col_penalty = find_vogels_penalty(C)
        max_row_penalty = max(row_penalty)
        max_col_penalty = max(col_penalty)

        # Determine if we allocate based on row or column penalty
        if max_row_penalty >= max_col_penalty:
            # Find the row with the maximum row difference
            row_idx = row_penalty.index(max_row_penalty)
            # Find the minimum element in that row which is not maxsize
            min_cost = min([c for c in C[row_idx] if c != maxsize])
            col_idx = C[row_idx].index(min_cost)

            # Allocate as much as possible to the selected cell
            allocation = min(S[row_idx], D[col_idx])
            answer += allocation * min_cost
            S[row_idx] -= allocation
            D[col_idx] -= allocation

            # Mark the row or column as unavailable if supply or demand is exhausted
            if S[row_idx] == 0:
                for j in range(len(C[row_idx])):
                    C[row_idx][j] = maxsize
            if D[col_idx] == 0:
                for i in range(len(C)):
                    C[i][col_idx] = maxsize

        else:
            # Find the column with the maximum penalty
            col_idx = col_penalty.index(max_col_penalty)
            # Find the minimum element in that column which is not maxsize
            min_cost = min([C[i][col_idx] for i in range(len(C)) if C[i][col_idx] != maxsize])
            row_idx = [C[i][col_idx] for i in range(len(C))].index(min_cost)

            # Allocate as much as possible to the selected cell
            allocation = min(S[row_idx], D[col_idx])
            answer += allocation * min_cost
            S[row_idx] -= allocation
            D[col_idx] -= allocation

            # Mark the row or column as unavailable if supply or demand is exhausted
            if S[row_idx] == 0:
                for j in range(len(C[row_idx])):
                    C[row_idx][j] = maxsize
            if D[col_idx] == 0:
                for i in range(len(C)):
                    C[i][col_idx] = maxsize

    print("Vogel's Approximation Method:", answer)

def north_west_corner(S, C, D):
    coeff = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    for i in range(len(C)):
        for j in range(len(C[0])):
            if C[i][j] != -1:
                coeff[i][j] = min(S[i], D[j])
                S[i] -= coeff[i][j]
                D[j] -= coeff[i][j]
                if S[i] == 0:
                    C = eliminate_row(C, i, coeff)
                if D[j] == 0:
                    C = eliminate_column(C, j, coeff)
    sum = 0
    for i in range(len(C)):
        for j in range(len(C[0])):
            sum += coeff[i][j] * C[i][j]
    print("\nNorth-West Corner Result:", sum)

if __name__ == "__main__":
    try:
        S, C, D = get_input()
        if not check_applicability(S, C, D):
            print("The method is not applicable!")
        elif sum(S) != sum(D):
            print("The problem is not balanced.")
        else:
            print_table(S, C, D)

            # Make copies of S, C, and D for each method
            S_nwc, C_nwc, D_nwc = copy.deepcopy(S), copy.deepcopy(C), copy.deepcopy(D)
            north_west_corner(S_nwc, C_nwc, D_nwc)

            S_vam, C_vam, D_vam = copy.deepcopy(S), copy.deepcopy(C), copy.deepcopy(D)
            vogels_approximation(S_vam, C_vam, D_vam)
    except ValueError:
        print("The method is not applicable!")


'''
Lab 7 Task 1
140 180 160
2 3 4 2 4
8 4 1 4 1
9 7 3 7 2
60 70 120 130 100

Lab 7 Task 2
160 140 170
7 8 1 2
4 5 9 8
9 2 3 6
120 50 190 110

Lab 7 Task 5
50 30 10
1 2 4 1
2 3 1 5
3 2 4 4
30 30 10 20

300 400 500
3 1 7 4
2 6 5 9
8 3 3 2
250 350 400 200
'''
