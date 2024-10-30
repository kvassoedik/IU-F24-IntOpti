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