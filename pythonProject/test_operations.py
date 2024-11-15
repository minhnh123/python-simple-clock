# test_math_operations.py
import pytest
from math_operations import add, subtract, multiply, divide

def test_add():
    assert add(3, 5) == 8
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(3, 7) == -4

def test_multiply():
    assert multiply(4, 3) == 12
    assert multiply(-1, 8) == -8

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ValueError):
        divide(10, 0)  # Testing division by zero
