from asyncio.windows_events import INFINITE
import sys
from sys import maxsize
import copy
import numpy as np

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

def get_solution(taken):
    b = {}
    rowsUsed = []
    colsUsed = []
    for i in range(len(taken)):
        for j in range(len(taken[0])):
            if taken[i][j]:
                b[(i, j)] = taken[i][j]
                rowsUsed.append(i)
                colsUsed.append(j)
    rowsUsed = sorted(list(set(rowsUsed)))
    colsUsed = sorted(list(set(colsUsed)))
     
    alphas = ["unknown" for _ in range(len(rowsUsed))]
    alphas[0] = 0
    betas = ["unknown" for _ in range(len(colsUsed))]
    while any(a == "unknown" for a in alphas) and any(be == "unknown" for be in betas):
        for k, v in b.items():
            if alphas[k[0]] != "unknown" and betas[k[1]] == "unknown":
                betas[k[1]] = v + alphas[k[0]]
            elif betas[k[1]]!= "unknown" and alphas[k[0]] == "unknown":
                alphas[k[0]] = betas[k[1]] - v
    print("Initial Solution Vector: ", end="")
    for alpha in alphas:
        print(alpha, end=" ")
    for beta in betas:
        print(beta, end=" ")
    print("\n")

def get_feasible_solution(allocation, C):
    A = []
    b = []

    for i in range(len(allocation)):
        for j in range(len(allocation[0])):
            if allocation[i][j] != 0:
                r = [0] * (len(allocation) + len(allocation[0]))
                r[i] = -1
                r[len(allocation) + j] = 1
                A.append(r)
                b.append(C[i][j])

    amount = len(A[0]) - len(A)
    for i in range(amount):
        r = [0] * (len(allocation) + len(allocation[0]))
        r[i] = 1
        A.append(r)
        b.append(0)

    try:
        sol = np.linalg.solve(np.array(A), np.array(b))
        print("Initial Feasible Solution: ", sol)
    except Exception:
        raise ValueError()



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
    #Initialize allocation matrix with zeros
    allocation = [[0] * len(D) for _ in range(len(S))]
    answer = 0 # Total cost
    cost = copy.deepcopy(C)

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
            allocation_amount = min(S[row_idx], D[col_idx])
            allocation[row_idx][col_idx] = allocation_amount # Track allocation
            answer += allocation_amount * min_cost
            S[row_idx] -= allocation_amount
            D[col_idx] -= allocation_amount

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
            allocation_amount = min(S[row_idx], D[col_idx])
            allocation[row_idx][col_idx] = allocation_amount # Track allocation
            answer += allocation_amount * min_cost
            S[row_idx] -= allocation_amount
            D[col_idx] -= allocation_amount

            # Mark the row or column as unavailable if supply or demand is exhausted
            if S[row_idx] == 0:
                for j in range(len(C[row_idx])):
                    C[row_idx][j] = maxsize
            if D[col_idx] == 0:
                for i in range(len(C)):
                    C[i][col_idx] = maxsize
    print("Vogel's Approximation Method:", answer)
    get_feasible_solution(allocation, cost)

def calculate_dual_variables(allocation, C):
    # Initialize alpha and beta arrays
    alphas = ["unknown" for _ in range(len(allocation))]
    betas = ["unknown" for _ in range(len(allocation[0]))]
    alphas[0] = 0 

    # Track allocations to assign alpha and beta values iteratively
    assigned = False
    while not assigned:
        assigned = True
        for i in range(len(allocation)):
            for j in range(len(allocation[0])):
                if allocation[i][j] != 0:  # Only for allocated cells
                    if alphas[i] != "unknown" and betas[j] == "unknown":
                        betas[j] = C[i][j] - alphas[i]
                    elif betas[j] != "unknown" and alphas[i] == "unknown":
                        alphas[i] = C[i][j] - betas[j]
                    elif alphas[i] == "unknown" or betas[j] == "unknown":
                        assigned = False  # Keep looping until all are assigned

    # Convert"unknown values to 0 (if any remain unassigned)
    alphas = [a if a != "unknown" else 0 for a in alphas]
    betas = [b if b != "unknown" else 0 for b in betas]

    # Return the solution vector
    return alphas + betas

def russells_approximation(S, C, D):
    supply = S[:]
    demand = D[:]
    allocation = [[0] * len(D) for _ in range(len(S))]
    total_cost = 0
    cost = copy.deepcopy(C)

    while any(supply) and any(demand):
        # Calculate row averages
        row_avg = []
        for row in C:
            valid_values = [c for c in row if c != sys.maxsize]
            row_avg.append(sum(valid_values) / len(valid_values) if valid_values else sys.maxsize)

        # Calculate column averages
        col_avg = []
        for j in range(len(D)):
            column_values = [C[i][j] for i in range(len(S)) if C[i][j] != sys.maxsize]
            col_avg.append(sum(column_values) / len(column_values) if column_values else sys.maxsize)

        # Calculate opportunity costs
        opportunity_costs = [
            [(C[i][j] - row_avg[i] - col_avg[j]) if C[i][j] != sys.maxsize else -sys.maxsize for j in range(len(D))]
            for i in range(len(S))
        ]

        # Find cell with the maximum opportunity cost
        max_cost = -sys.maxsize
        max_i, max_j = -1, -1
        for i in range(len(S)):
            for j in range(len(D)):
                if opportunity_costs[i][j] > max_cost:
                    max_cost = opportunity_costs[i][j]
                    max_i, max_j = i, j

        # Exit if no valid cell found (shouldn't happen unless all are exhausted)
        if max_i == -1 or max_j == -1:
            break

        # Allocate as much as possible
        allocation_amount = min(supply[max_i], demand[max_j])
        allocation[max_i][max_j] = allocation_amount
        total_cost += allocation_amount * C[max_i][max_j]

        # Update supply and demand
        supply[max_i] -= allocation_amount
        demand[max_j] -= allocation_amount

        # Mark exhausted rows or columns
        if supply[max_i] == 0:
            for j in range(len(D)):
                C[max_i][j] = sys.maxsize
        if demand[max_j] == 0:
            for i in range(len(S)):
                C[i][max_j] = sys.maxsize

    # Calculate dual variables (solution vector)
    solution_vector = calculate_dual_variables(allocation, cost)

    print("\nRussell's Approximation Method:", total_cost)

    print("Initial Solution Vector:", solution_vector)

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
    sol = [[0 for _ in range(len(C[0]))] for _ in range(len(C))]
    for i in range(len(coeff)):
        for j in range(len(coeff[0])):
            if coeff[i][j] != 0:
                sol[i][j] = C[i][j]
    get_solution(sol)

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

            S_russell, C_russell, D_russell = copy.deepcopy(S), copy.deepcopy(C), copy.deepcopy(D)
            russells_approximation(S_russell, C_russell, D_russell)
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

100 150 200
5 8 6 7
6 7 8 5
7 5 6 8
120 130 100 100
'''