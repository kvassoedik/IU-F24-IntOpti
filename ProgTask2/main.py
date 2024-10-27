from matrixMethods import *


def interiorPoint(x, A, c, alpha):
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
    return multiply(D, x_)


if __name__ == "__main__":
    x = [1/2, 7/2, 1, 2]
    A = [[2, 4, 1, 0], [1, 3, 0, -1]]
    c = [[1], [1], [0], [0]]
    for i in range(1, 6):
        x = vectorOfMatrix(interiorPoint(x, A, c, 0.5))
        print(f'Iteration {i}: {x}')
