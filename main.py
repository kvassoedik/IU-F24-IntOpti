import numpy as np
from simplexMethods import findPivot, replaceVars
from utils import printTable, roundTable

# Input from the user
def get_input():
    # Coefficients of the objective function
    C = list(map(float, input("Enter the coefficients of the objective function separated by spaces: ").split()))

    # Coefficients of the constraints
    num_constraints = int(input("Enter the number of constraints: "))
    A = []
    for i in range(num_constraints):
        constraint = list(map(float, input(f"Enter the coefficients of constraint {i+1} separated by spaces: ").split()))
        A.append(constraint)

    # Right-hand side of constraints
    b = list(map(float, input("Enter the right-hand side of the constraints separated by spaces: ").split()))

    # Input for the number of decimal places to round to
    accuracy = int(input("Enter the number of digits after decimal point: "))

    return C, A, b, accuracy

# Check if Simplex method can be applied (checking linearity)
def check_linearity(C, A, b):
    try:
        # Ensure that all inputs are numerical
        C = np.array(C, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        # Check the shapes of the arrays (compatibility of dimensions of the matrices and vectors)
        if A.shape[0] != len(b) or A.shape[1] != len(C):
            return "The method is not applicable"
        
        return "The method is applicable."
    except:
        return "The method is not applicable."

# Initial table creation
def create_initial_table(C, A, b, accuracy):
    # Number of variables and constraints
    num_terms = len(b)
    
    # Add the objective row (with negated C)
    objective_row = C
    for i in range(len(objective_row)):
        objective_row[i] = -objective_row[i]
    objective_row.append(0)
    
    # Combine the objective and constraints into the final table
    table = []
    table.append(objective_row)
    for i in range(num_terms):
        A[i].append(b[i])
        table.append(A[i])
    
    # Round to the specified accuracy
    table = roundTable(table, accuracy)

    return table    

def get_solution(table, num_vars):

    # Number of decision variables (excluding slack variables)
    # Subtract 1 for the right-hand side column
    
    # Initialize the solution vector
    solution = [0] * num_vars

    for j in range(num_vars):
        col = [table[i][j] for i in range(1, len(table))]
        
        # Check if the column corresponds to a basic variable
        if col.count(1) == 1 and col.count(0) == len(col) - 1:
            # Get the row where the value is 1
            row = col.index(1)
            solution[j] = table[row + 1][-1]  # Right-hand side value

    return solution            

if __name__ == "__main__":
    C, A, b, accuracy = get_input()
    
    linear_check = check_linearity(C, A, b)
    if linear_check == "The method is applicable.":
        initial_table = create_initial_table(C, A, b, accuracy)

        # To display the number of decimals
        np.set_printoptions(formatter={'float_kind': lambda x: f"{x:.{accuracy}f}"})

        print("Initial Simplex Table:")
        printTable(initial_table, accuracy)

        table = initial_table.copy()
        iteration = 0

        while any(elem < 0 for elem in table[0][:-1]):
            iteration += 1
            pivot = findPivot(table)
            table = replaceVars(table, pivot[0], pivot[1])
            print()
            print(f"Iteration {iteration}:")
            printTable(table, accuracy)

        num_vars = len(C) - C.count(0) - 1
        solution = get_solution(table, num_vars)
        objective_value = table[0][-1]

        print("Optimal solution (decision variables):", np.round(solution, accuracy))
        print(f"Optimal value of the objective function: {objective_value:.{accuracy}f}")

    else:
        print(linear_check)
