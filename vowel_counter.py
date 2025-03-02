# vowel_counter.py

def count_vowels(s):
    """Возвращает количество гласных в строке s."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)