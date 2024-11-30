def f(func, x):
    res = 0
    func = func[::-1]
    for i in range(len(func) - 1, -1, -1):
        res += func[i] * (x ** i)
    return res

def inp():
    func = input("Enter coefficients for x^i for decreasing i separated by spaces: ").split(" ")
    func = [float(x) for x in func]
    a, b = input("a, b interval separated by a space: ").split(" ")
    eps = float(input("Tolerance value: "))
    return func, float(a), float(b), eps

def bisec():
    func, a, b, eps = inp()
    while abs(b - a) >= eps:
        c = (a + b) / 2
        if f(func, c) == 0:
            return c
        if (f(func, c) <= 0 and f(func, a) <= 0) or (f(func, c) >= 0 and f(func, a) >= 0):
            a = c
        else:
            b = c
    return (a + b) / 2

def goldsec():
    func, a, b, eps = inp()
    alpha = (5 ** 0.5 - 1) / 2
    while abs(b - a) >= eps:
        x1 = b - alpha * (b - a)
        x2 = a + alpha * (b - a)
        if f(func, x1) > f(func, x2):
            a = x1
        elif f(func, x1) < f(func, x2):
            b = x2
        else:
            a = x1
            b = x2
    return (a + b) / 2, f(func, (a + b) / 2)

def grad_ascent():
    # Function and its derivative
    def f(x):
        return -x**2 + 4*x + 1
    
    def derivative(x):
        return -2*x + 4

    # User inputs
    x0 = float(input("Enter initial guess x0: "))
    alpha = float(input("Enter learning rate alpha: "))
    N = int(input("Enter number of iterations N: "))
    
    # Gradient ascent logic
    x = x0
    for i in range(N):
        gradient = derivative(x) # Calculate gradient
        x = x + alpha * gradient  # Update x using gradient ascent rule
    
    return x, f(x)

if __name__ == "__main__":
    print("BISECTION METHOD")
    print(f"Approximate root: {bisec()}")

    print()

    print("GOLDEN SECTION METHOD")
    gsx, gsf = goldsec()
    print(f"Minimum x: {gsx}, Minimum function value: {gsf}")

    print()

    print("GRADIENT ASCENT METHOD")
    max_x, max_f = grad_ascent()
    print(f"Maximum x: {max_x}, Maximum function value: {max_f}")

"""
TESTING

Bisection
1 -6 11 -6
1 2
0.000001

Golden Section
1 -4 7
0 5
0.0001

Gradient Ascent
0
0.1
100
"""