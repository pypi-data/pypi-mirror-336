# vickycalulator/calculations.py

def add(a, b):
    """
    Return the sum of a and b.
    """
    return a + b

def subtract(a, b):
    """
    Return the difference of a and b.
    """
    return a - b

def multiply(a, b):
    """
    Return the product of a and b.
    """
    return a * b

def divide(a, b):
    """
    Return the quotient of a and b.
    Raises ZeroDivisionError if b == 0.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b
