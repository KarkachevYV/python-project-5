import asyncio
import logging
import aiosqlite
import aiohttp
import json
import random

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
# from states import FinancesForm

from config import API_TOKEN

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
logging.basicConfig(level=logging.INFO)

# Определение состояний
class FinancesForm(StatesGroup):
    category1 = State()
    expenses1 = State()
    category2 = State()
    expenses2 = State()
    category3 = State()
    expenses3 = State()
    category4 = State()
    expenses4 = State()
    category5 = State()
    expenses5 = State()

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация в телеграм-боте"), KeyboardButton(text="Курс валют")],
        [KeyboardButton(text="Советы по экономии"), KeyboardButton(text="Личные финансы")]
    ],
    resize_keyboard=True
)

# Создание базы данных
async def setup_db():
    db = await aiosqlite.connect('user.db')
    await db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            name TEXT,
            category1 TEXT,
            category2 TEXT,
            category3 TEXT,
            category4 TEXT,
            category5 TEXT,
            expenses1 REAL,
            expenses2 REAL,
            expenses3 REAL,
            expenses4 REAL,
            expenses5 REAL
        )
    ''')
    await db.commit()
    await db.close()  # Закрываем соединение
    print("✅ База данных инициализирована.")

async def get_db():
    return await aiosqlite.connect('user.db')


# Команда /start
@router.message(Command("start"))
async def send_start(message: Message):
    await message.answer("Привет! Я ваш личный финансовый помощник. Выберите одну из опций в меню:", reply_markup=keyboard)

# Команда /help
@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "🛠 Доступные команды:\n\n"
        "📌 /start — Запустить бота.\n"
        "📌 /help — Показать это сообщение.\n"
    )

# Регистрация пользователя
@router.message(F.text == "Регистрация в телеграм-боте")
async def registration(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name

    db = await get_db()  # Получаем соединение с БД

    async with db.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,)) as cursor:
        user = await cursor.fetchone()

    if user:
        await message.answer("Вы уже зарегистрированы!")
    else:
        await db.execute('INSERT INTO users (telegram_id, name) VALUES (?, ?)', (telegram_id, name))
        await db.commit()
        await message.answer("Вы успешно зарегистрированы!")

    await db.close()  # Закрываем соединение после работы


# Получение курса валют (асинхронный запрос через aiohttp)
@router.message(lambda message: message.text == "Курс валют")
async def exchange_rates(message: Message):
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.text()  # Получаем данные как текст
            data = json.loads(data)  # Преобразуем текст в JSON

            # data = await response.json()
            usd_to_rub = data["Valute"]["USD"]["Value"]
            eur_to_rub = data["Valute"]["EUR"]["Value"]

            await message.answer(f"💵 1 USD = {usd_to_rub:.2f} RUB\n💶 1 EUR = {eur_to_rub:.2f} RUB")

@router.message(F.text == "Советы по экономии")
async def send_tips(message: Message):
   tips = [
       "Совет 1. Контроль доходов и расходов: \nВедите учёт трат таблица, приложение или просто заметки. \nАнализируйте, на что уходит больше всего денег, и где можно сократить. \nОпределите необязательные траты и попробуйте от них отказаться.",
       "Совет 2. Оптимизация расходов: \nПокупки по акциям и скидкам, но без импульсивных решений. \nИспользуйте кэшбэк и бонусные программы. \nПланируйте крупные траты заранее, избегая переплат. \nНе берите кредиты на вещи, которые не приносят доход.",
       "Совет 3. Оптимизация регулярных платежей: \nПроверьте тарифы ЖКХ, связи, интернета — возможно, есть более выгодные. \nЕсли есть подписки, стриминг, софт — нужны ли все? \nМожно ли заменить бесплатными альтернативами?",
       "Совет 4. Разумные привычки: \nГотовьте еду дома — это дешевле, чем заказывать.\nПокупайте товары оптом или по скидке, если это действительно нужно.\nПродавайте ненужные вещи вместо того, чтобы выбрасывать.",
       "Совет 5. Сбережения и инвестиции:\nОткладывайте минимум 10% дохода (или больше, если возможно).\nСоздайте финансовую подушку (3–6 месячных расходов).\nРассмотрите инвестиции, но только после изучения темы (депозиты, облигации, акции)."
   ]
   tip = random.choice(tips)
   await message.answer(tip)

# Старт ввода категорий
@router.message(F.text == "Личные финансы")
async def finances_start(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.reply("Введите первую категорию расходов:")

# Ввод категории 1
@router.message(FinancesForm.category1)
async def finances_category1(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.reply("Введите расходы для категории 1:")

# Ввод расходов 1
@router.message(FinancesForm.expenses1)
async def finances_expenses1(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.reply("Введите вторую категорию расходов:")

# Ввод категории 2
@router.message(FinancesForm.category2)
async def finances_category2(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.reply("Введите расходы для категории 2:")

# Ввод расходов 2
@router.message(FinancesForm.expenses2)
async def finances_expenses2(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.reply("Введите третью категорию расходов:")

# Ввод категории 3
@router.message(FinancesForm.category3)
async def finances_category3(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.reply("Введите расходы для категории 3:")

# Ввод расходов 3
@router.message(FinancesForm.expenses3)
async def finances_expenses3(message: Message, state: FSMContext):
    await state.update_data(expenses3=float(message.text))
    await state.set_state(FinancesForm.category4)
    await message.reply("Введите четвёртую категорию расходов:")

# Ввод категории 4
@router.message(FinancesForm.category4)
async def finances_category4(message: Message, state: FSMContext):
    await state.update_data(category4=message.text)
    await state.set_state(FinancesForm.expenses4)
    await message.reply("Введите расходы для категории 4:")

# Ввод расходов 4
@router.message(FinancesForm.expenses4)
async def finances_expenses4(message: Message, state: FSMContext):
    await state.update_data(expenses4=float(message.text))
    await state.set_state(FinancesForm.category5)
    await message.reply("Введите пятую категорию расходов:")

# Ввод категории 5
@router.message(FinancesForm.category5)
async def finances_category5(message: Message, state: FSMContext):
    await state.update_data(category5=message.text)
    await state.set_state(FinancesForm.expenses5)
    await message.reply("Введите расходы для категории 5:")


@router.message(FinancesForm.expenses5)
async def finances(message: Message, state: FSMContext):
   await state.update_data(expenses5=float(message.text))
   data = await state.get_data()
   telegram_id = message.from_user.id

   db = await get_db()
   await db.execute('''UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, category3 = ?, expenses3 = ?, category4 = ?, expenses4 = ?, category5 = ?, expenses5 = ? WHERE telegram_id = ?''',
                  (data['category1'], data['expenses1'], data['category2'], data['expenses2'], data['category3'], data['expenses3'], data['category4'], data['expenses4'], data['category5'], data["expenses5"], telegram_id))
   await db.commit() 

   await message.answer("Категории и расходы сохранены!")
   await db.close() # Закрываем соединение после работы
   await state.clear()

# Основная функция запуска бота
async def main():
    await setup_db()
    dp.include_router(router)

    print("🚀 Бот запущен! Нажмите Ctrl + C для выхода.")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        dp.shutdown()
        await bot.session.close()
        print("✅ Сессия бота закрыта.")

# Запуск
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Бот выключен через Ctrl + C.")
