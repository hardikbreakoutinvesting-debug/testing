"""
calculator/operations.py
Core arithmetic operations for the calculator app.
"""


class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Return the quotient of a divided by b.

    Raises:
        CalculatorError: If b is zero.
    """
    if b == 0:
        raise CalculatorError("Division by zero is not allowed.")
    return a / b


def power(base: float, exponent: float) -> float:
    """Return base raised to the power of exponent."""
    return base ** exponent


def modulo(a: float, b: float) -> float:
    """
    Return the remainder of a divided by b.

    Raises:
        CalculatorError: If b is zero.
    """
    if b == 0:
        raise CalculatorError("Modulo by zero is not allowed.")
    return a % b


# Map operation names to functions for easy API dispatch
OPERATIONS = {
    "add":      add,
    "subtract": subtract,
    "multiply": multiply,
    "divide":   divide,
    "power":    power,
    "modulo":   modulo,
}


def calculate(operation: str, a: float, b: float) -> float:
    """
    Dispatch a named operation.

    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide', 'power', 'modulo'.
        a: First operand.
        b: Second operand.

    Returns:
        Result of the operation.

    Raises:
        CalculatorError: If the operation name is unknown.
    """
    op_func = OPERATIONS.get(operation)
    if op_func is None:
        raise CalculatorError(
            f"Unknown operation '{operation}'. "
            f"Supported: {', '.join(OPERATIONS.keys())}"
        )
    return op_func(a, b)
