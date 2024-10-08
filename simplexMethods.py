def printTable(table, accuracy):
    table = roundTable(table, accuracy)
    for line in table:
        for elem in line:
            print(str(elem) + "\t", end="")
        print()

def findMinInd(arr):
    minInd = 0
    for i in range(len(arr)):
        if arr[i] < arr[minInd]:
            minInd = i
    return minInd

def roundTable(table, accuracy):
    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = round(table[i][j], accuracy)
    return table

def findPivot(table):
    pivotCol = findMinInd(table[0])
    ratios = []
    for i in range(1, len(table)):
        if table[i][pivotCol] == 0:
            ratios.append(1000000)
        else:
            ratios.append(table[i][-1] / table[i][pivotCol])
    pivotRow = findMinInd(ratios)
    return [pivotRow + 1, pivotCol]

def replaceVars(table, pivotRow, pivotCol):
    newTable = table.copy()

    div = table[pivotRow][pivotCol]
    for i in range(len(table[pivotRow])):
        newTable[pivotRow][i] = table[pivotRow][i] / div
    
    for i in range(len(table)):
        if i != pivotRow:
            piv = newTable[pivotRow][pivotCol] * table[i][pivotCol]
            for j in range(len(table[i])):
                newTable[i][j] = table[i][j] - newTable[pivotRow][j] * piv 

    return(newTable)