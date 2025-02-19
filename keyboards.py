from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="Тестовая кнопка 1")],
#     [KeyboardButton(text="Тестовая кнопка 2"), KeyboardButton(text="Тестовая кнопка 3")]
# ], resize_keyboard=True)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
], resize_keyboard=True)

# inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
#    [InlineKeyboardButton(text="Каталог", callback_data='catalog')],
#    [InlineKeyboardButton(text="Новости", callback_data='news')],
#    [InlineKeyboardButton(text="Профиль", callback_data='profile')],
# ])


# inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
#    [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=epLg__rBZ38')],
#    [InlineKeyboardButton(text="Новости", url='https://life.ru/s/novosti/last')],
#    [InlineKeyboardButton(text="Музыка", url='https://dzen.ru/video/watch/618a25a7e9efa72da9763a42?utm_referrer=yandex.ru')],
# ])

# test = ["кнопка 1", "кнопка 2", "кнопка 3", "кнопка 4"]

# async def test_keyboard():
#    keyboard = ReplyKeyboardBuilder()
#    for key in test:
#      keyboard.add(KeyboardButton(text=key))
#    return keyboard.adjust(2).as_markup()

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data='further')],
  
])


test = ["Опция 1", "Опция 2"]



async def test_keyboard():
   keyboard = InlineKeyboardBuilder()
   for key in test:
     keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
   return keyboard.adjust(2).as_markup()

# async def test_keyboard():
#    keyboard = InlineKeyboardBuilder()
#    for key in test:
#      keyboard.add(InlineKeyboardButton(text=key, url='https://www.youtube.com/watch?v=epLg__rBZ38'))
#    return keyboard.adjust(2).as_markup()