def multiply(m1, m2):
    m = [[0 for _ in range(len(m2[0]))] for _ in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            indexSum = 0
            for k in range(len(m1[0])):
                indexSum += m1[i][k] * m2[k][j]
            m[i][j] = indexSum
    return m


def multiplyByScalar(matrix, scalar):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = matrix[i][j] * scalar
    return matrix


def transpose(m):
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]


def diagonal(vector):
    matrix = [[0 for _ in range(len(vector))] for _ in range(len(vector))]
    for i in range(len(vector)):
        matrix[i][i] = vector[i]
    return matrix


def identity(n):
    return diagonal([1 for _ in range(n)])


def ones(n):
    return [[1] for _ in range(n)]


def vectorOfMatrix(matrix):
    vector = []
    for i in range(len(matrix)):
        vector.append(matrix[i][0])
    return(vector)


def maxABS(matrix):
    m = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] < 0 and abs(matrix[i][j]) > m:
                m = abs(matrix[i][j])
    return m


def add(matrix1, matrix2):
    m = [[0 for _ in range(len(matrix1[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            m[i][j] = matrix1[i][j] + matrix2[i][j]
    return m


def subtract(matrix1, matrix2):
    m = [[0 for _ in range(len(matrix1[0]))] for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            m[i][j] = matrix1[i][j] - matrix2[i][j]
    return m


def minor(matrix, i, j):
    minor = []
    for k in matrix[:i] + matrix[i + 1:]:
        minor.append(k[:j] + k[j + 1:])
    return minor


def cofactor(matrix):
    cof = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            row.append(matrix[i][j] * ((-1) ** (i + j + 2)))
        cof.append(row)
    return cof


def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if len(matrix) == 1:
        return matrix[0][0]
    d = 0
    for i in range(len(matrix)):
        d += matrix[0][i] * (-1) ** i * determinant(minor(matrix, 0, i))
    return d


def inverse(matrix):
    min = [[determinant(minor(matrix, i, j)) for j in range(len(matrix[0]))] for i in range(len(matrix))]

    cof = cofactor(min)
    return multiplyByScalar(transpose(cof), 1/determinant(matrix))