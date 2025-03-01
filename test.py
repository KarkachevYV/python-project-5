#test.py
import pytest
from main_test import  check, is_palindrome, sort_list

def test_check():
    assert check(6) == True

def test_check2():
   assert check(3) == False

@pytest.mark.parametrize("number, expected", [
   (2, True),
   (5, False),
   (0, True),
   (56, True),
   (-3, False)
])

def test_check_with_param(number, expected):
   assert check(number) == expected

def test_isPalindrome_true():
    assert is_palindrome('madam') == True

def test_isPalindrome_false():
    assert is_palindrome('hello') == False

@pytest.mark.parametrize("test_input, expected", [
    ('level', True),
    ('python', False),
    ('racecar', True),
    ('', True),
])
def test_isPalindrome(test_input, expected):
    assert is_palindrome(test_input) == expected


def test_sort1():
    assert sort_list([-1, 3, 0, -2, 2]) == [-2, -1, 0, 2, 3]

def test_sort2():
    assert sort_list([5, 6, 3, 1, 2]) == [1, 2, 3, 5, 6]