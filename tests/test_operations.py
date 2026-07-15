"""
tests/test_operations.py
Unit tests for calculator/operations.py
"""

import pytest
from calculator.operations import (
    add, subtract, multiply, divide,
    power, modulo, calculate, CalculatorError,
)


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAdd:
    def test_add_positive(self):
        assert add(3, 5) == 7

    def test_add_negative(self):
        assert add(-1, -2) == -3

    def test_add_floats(self):
        assert add(1.5, 2.5) == pytest.approx(4.0)

    def test_add_zero(self):
        assert add(0, 0) == 0


# ---------------------------------------------------------------------------
# subtract
# ---------------------------------------------------------------------------

class TestSubtract:
    def test_subtract_positive(self):
        assert subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        assert subtract(3, 7) == -4

    def test_subtract_floats(self):
        assert subtract(5.5, 2.5) == pytest.approx(3.0)


# ---------------------------------------------------------------------------
# multiply
# ---------------------------------------------------------------------------

class TestMultiply:
    def test_multiply_positive(self):
        assert multiply(3, 4) == 12

    def test_multiply_by_zero(self):
        assert multiply(99, 0) == 0

    def test_multiply_negative(self):
        assert multiply(-3, 4) == -12

    def test_multiply_floats(self):
        assert multiply(2.5, 4) == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# divide
# ---------------------------------------------------------------------------

class TestDivide:
    def test_divide_positive(self):
        assert divide(10, 2) == 5.0

    def test_divide_floats(self):
        assert divide(7, 2) == pytest.approx(3.5)

    def test_divide_by_zero_raises(self):
        with pytest.raises(CalculatorError, match="Division by zero"):
            divide(5, 0)

    def test_divide_negative(self):
        assert divide(-9, 3) == -3.0


# ---------------------------------------------------------------------------
# power
# ---------------------------------------------------------------------------

class TestPower:
    def test_power_positive(self):
        assert power(2, 10) == 1024

    def test_power_zero_exponent(self):
        assert power(99, 0) == 1

    def test_power_fractional(self):
        assert power(4, 0.5) == pytest.approx(2.0)

    def test_power_negative_base(self):
        assert power(-2, 3) == -8


# ---------------------------------------------------------------------------
# modulo
# ---------------------------------------------------------------------------

class TestModulo:
    def test_modulo_positive(self):
        assert modulo(10, 3) == 1

    def test_modulo_even(self):
        assert modulo(10, 5) == 0

    def test_modulo_by_zero_raises(self):
        with pytest.raises(CalculatorError, match="Modulo by zero"):
            modulo(10, 0)


# ---------------------------------------------------------------------------
# calculate (dispatcher)
# ---------------------------------------------------------------------------

class TestCalculate:
    def test_dispatch_add(self):
        assert calculate("add", 1, 2) == 3

    def test_dispatch_subtract(self):
        assert calculate("subtract", 5, 3) == 2

    def test_dispatch_multiply(self):
        assert calculate("multiply", 4, 5) == 20

    def test_dispatch_divide(self):
        assert calculate("divide", 10, 4) == pytest.approx(2.5)

    def test_dispatch_power(self):
        assert calculate("power", 3, 3) == 27

    def test_dispatch_modulo(self):
        assert calculate("modulo", 7, 3) == 1

    def test_unknown_operation_raises(self):
        with pytest.raises(CalculatorError, match="Unknown operation"):
            calculate("sqrt", 9, 0)
