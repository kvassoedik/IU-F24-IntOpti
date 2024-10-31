import numpy as np
from matrixMethods import *
from ProgTask1.main import simplex

def list_to_column(c, A, b):
    # Convert lists into column vector format
    c = [[ci] for ci in c]
    b = [[bi] for bi in b]
    return c, A, b

def roundTable(table, accuracy):
    # Rounds each element in the table to the specified accuracy
    return [[round(value, accuracy) for value in row] for row in table]

def get_user_input():
    # Coefficients of the objective function
    c = list(map(float, input("Enter the coefficients of the objective function separated by spaces: ").split()))

    # Coefficients of the constraints
    num_constraints = int(input("Enter the number of constraints: "))
    A = []
    for i in range(num_constraints):
        row = list(map(float, input(f"Enter the coefficients of constraint {i+1} separated by spaces: ").split()))
        A.append(row)

    # Right-hand side of constraints
    b = list(map(float, input("Enter the right-hand side of the constraints separated by spaces: ").split()))

    # Input for the number of decimal places to round to
    accuracy = int(input("Enter the number of digits after decimal point: "))

    # Initial starting point for x (manual input)
    x = list(map(float, input("Enter the initial starting point for x separated by spaces: ").split()))

    c, A, b = list_to_column(c, A, b)

    return c, A, b, accuracy, x

def interior_point(x, A, c, alpha, accuracy):
    D = diagonal(x)
    A_ = multiply(A, D)
    c_ = multiply(D, c)
    A_T = transpose(A_)
    m1 = inverse(multiply(A_, A_T))
    m2 = multiply(A_T, m1)
    m3 = multiply(m2, A_)
    P = subtract(identity(len(x)), m3)
    c_P = multiply(P, c_)
    x_ = add(ones(len(x)), multiplyByScalar(c_P, alpha / maxABS(c_P)))
    
    # Round to the specified accuracy
    return roundTable(multiply(D, x_), accuracy)

def dumbRound(vector, accuracy):
    return [round(value, accuracy) for value in vector] 

if __name__ == "__main__":
    # Getting user input
    c, A, b, accuracy, x = get_user_input()

    alpha_values = [0.5, 0.9]
    
    # To display the number of decimals
    np.set_printoptions(formatter={'float_kind': lambda x: f"{x:.{accuracy}f}"})
    
    # Running the Interior-Point method for each alpha
    for alpha in alpha_values:
        print(f"\nResults for α = {alpha}")
        i = 1
        x_old = x
        while True:  # 5 iterations
            # Perform the interior point computation
            x_new = vectorOfMatrix(interior_point(x_old, A, c, alpha, accuracy))
            print(f'Iteration {i} with α = {alpha}: {x_new}')
            
            if dumbRound(x_new, 3) == dumbRound(x_old, 3):
                break

            x_old = x_new
            
            i += 1

    c_simp = transpose(c)[0]
    b_simp = transpose(b)[0]
    print("\nSIMPLEX METHOD")
    simplex(c_simp, A, b_simp, accuracy)

'''
Lab 5 Task 1
1 1 0 0
2
2 4 1 0
1 3 0 -1
16 9
7
0.5 3.5 1 2

Lab 3 Task 1??
9 10 16 0 0 0
3
18 15 12 1 0 0
6 4 8 0 1 0
5 3 3 0 0 1
360 192 180
7
1 1 1 315 174 169

'''
