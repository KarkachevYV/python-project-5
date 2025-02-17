from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тестовая кнопка 1")],
    [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=epLg__rBZ38')]
])

test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

async def test_keyboard():
   keyboard = ReplyKeyboardBuilder()
   for key in test:
     keyboard.add(KeyboardButton(text=key))
   return keyboard.adjust(2).as_markup()