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
        elif sum(S)!= sum(D):
            print("The problem is not balanced.")
        else:
            print_table(S, C, D)
            north_west_corner(S, C, D)
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
'''
