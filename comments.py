import re

def is_russian_palindrome(comment):
    # Подготовка строки: удаление пробелов, знаков препинания и приведение к нижнему регистру
    # Символы, которые остаются: буквы русского алфавита и цифры
    comment = re.sub(r'[^а-яА-Я0-9]', '', comment).lower()
    
    # Проверка с использованием срезов
    return comment == comment[::-1]

# Примеры использования
print(is_russian_palindrome("А роза упала на лапу Азора"))  # Выведет: True
print(is_russian_palindrome("Это не палиндром"))  # Выведет: False

def is_palindrome(s):
    # 1. Подготовка строки: удаление пробелов и неалфавитных символов, приведение к нижнему регистру
    s = re.sub(r'[^A-Za-z0-9]', '', s).lower()

    # 2. Инициализация указателей
    left, right = 0, len(s) - 1

    # 3. Проверка символов с использоваием указателей
    while left < right:
        if s[left] != s[right]:
            return False  # Строка не является палиндромом
        left += 1
        right -= 1

    # 4. Результат: строка является палиндромом
    return True

# Пример использования
print(is_palindrome("A man, a plan, a canal, Panama"))  # Выведет: True
print(is_palindrome("Hello, World!"))  # Выведет: False

def is_palindrome(s):
    # Подготовка строки
    s = re.sub(r'[^A-Za-z0-9]', '', s).lower()
    # Проверка с использованием функции reversed
    return s == ''.join(reversed(s))

# Пример использования
print(is_palindrome("A man, a plan, a canal, Panama"))  # Выведет: True
print(is_palindrome("Hello, World!"))  # Выведет: False
def is_palindrome(s):
    # Подготовка строки
    s = re.sub(r'[^A-Za-z0-9]', '', s).lower()
    # Проверка, сравнивая первую половину с перевернутой второй половиной
    mid = len(s) // 2
    return s[:mid] == s[-1:-(mid+1):-1]

# Пример использования
print(is_palindrome("A man, a plan, a canal, Panama"))  # Выведет: True
print(is_palindrome("Hello, World!"))  # Выведет: False

from collections import deque

def is_palindrome(s):
    # Подготовка строки
    s = re.sub(r'[^A-Za-z0-9]', '', s).lower()
    # Преобразование строки в дек
    d = deque(s)
    # Проверка, извлекая элементы с обоих концов
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True

# Пример использования
print(is_palindrome("A man, a plan, a canal, Panama"))  # Выведет: True
print(is_palindrome("Hello, World!"))  # Выведет: False