# test_vowel_counter.py
import pytest
from vowel_counter import count_vowels

def test_count_vowels():
    assert count_vowels("Hello") == 2  # "e", "o"
    assert count_vowels("Pytest") == 1  # "e"
    assert count_vowels("AEIOU") == 5  # "A", "E", "I", "O", "U"
    assert count_vowels("bcdfg") == 0  # нет гласных
    assert count_vowels("") == 0  # пустая строка
    assert count_vowels("Python is fun!") == 3  # "o", "i", "u"
