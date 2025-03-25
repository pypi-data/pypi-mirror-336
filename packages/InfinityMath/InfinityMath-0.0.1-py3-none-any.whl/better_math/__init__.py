import math
import cmath  # Для комплексних чисел
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad  # Для чисельного інтегрування

def sqrt(x):
    return math.sqrt(x)

def pow(x, n):
    return x**n

def sum(x1, x2):
    return x1 + x2

def subtraction(x1, x2):
    return x1 - x2

def product(x1, x2):
    return x1 * x2

def div(x1, x2):
    if x2 == 0:
        raise ValueError("Division by zero is not allowed")
    return x1 / x2

def factorial(x):
    return math.factorial(x)

def log(x, base=10):
    return math.log(x, base)

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def tan(x):
    return math.tan(x)

def asin(x):
    return math.asin(x)

def acos(x):
    return math.acos(x)

def atan(x):
    return math.atan(x)

def solve_quadratic(a, b, c):
    D = (b ** 2) - (4 * a * c)
    if D >= 0:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
    else:
        x1 = (-b + cmath.sqrt(D)) / (2 * a)
        x2 = (-b - cmath.sqrt(D)) / (2 * a)
    return x1, x2

def viet_quadratic(x1, x2):
    p = -1 * (x1 + x2)
    q = x1 * x2
    return p, q

def integrate_function(func, a, b):
    result, _ = quad(func, a, b)
    return result

def plot_function(func, x_range, label="f(x)", color="b"):
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = func(x)
    plt.plot(x, y, color, label=label)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_multiple_functions(functions, x_range, labels=None, colors=None):
    x = np.linspace(x_range[0], x_range[1], 1000)
    plt.figure()
    if labels is None:
        labels = [f"f{x}" for x in range(1, len(functions) + 1)]
    if colors is None:
        colors = ["b", "g", "r", "c", "m", "y", "k"] * 2  # Повторюваний список кольорів
    for func, label, color in zip(functions, labels, colors):
        y = func(x)
        plt.plot(x, y, color, label=label)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    print("Тестуємо функції:")
    print("Квадратний корінь з 16:", sqrt(16))
    print("2 в 3 степені:", pow(2, 3))
    print("Сума 5 і 3:", sum(5, 3))
    print("Різниця 10 і 4:", subtraction(10, 4))
    print("Добуток 7 і 8:", product(7, 8))
    print("Ділення 9 на 3:", div(9, 3))
    print("Факторіал 5:", factorial(5))
    print("Розв’язок рівняння 2x² + 3x - 2 = 0:", solve_quadratic(2, 3, -2))
    print("Знаходження коефіцієнтів для x1=2, x2=3:", viet_quadratic(2, 3))
    print("Інтеграл x^2 від 0 до 2:", integrate_function(lambda x: x**2, 0, 2))
