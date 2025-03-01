#main_test.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b


def remnant(a, b):
    if b == 0:
        raise ValueError("Деление на ноль недопустимо.")
    return a % b

# def remnant(a, b):
#     return a % b