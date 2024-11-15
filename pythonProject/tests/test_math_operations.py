import pytest
from math_operations import add, subtract, multiply, divide, power, percentage

def test_add():
    assert add(3, 5) == 9  # Thay đổi 8 thành 9 để gây lỗi
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(3, 7) == -4
    assert subtract(0, 0) == 0

def test_multiply():
    assert multiply(4, 3) == 12
    assert multiply(-1, 8) == -8
    assert multiply(0, 5) == 0

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ValueError):
        divide(10, 0)

def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(-2, 2) == 4

def test_percentage():
    assert percentage(200, 10) == 20
    assert percentage(50, 20) == 10
    assert percentage(0, 100) == 0
