import asyncio
import logging
import aiosqlite
import aiohttp

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

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
    async with aiosqlite.connect('user.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                name TEXT,
                category1 TEXT,
                category2 TEXT,
                category3 TEXT,
                expenses1 REAL,
                expenses2 REAL,
                expenses3 REAL
            )
        ''')
        await db.commit()
    print("✅ База данных инициализирована.")

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

    async with aiosqlite.connect('user.db') as db:
        async with db.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,)) as cursor:
            user = await cursor.fetchone()

        if user:
            await message.answer("Вы уже зарегистрированы!")
        else:
            await db.execute('INSERT INTO users (telegram_id, name) VALUES (?, ?)', (telegram_id, name))
            await db.commit()
            await message.answer("Вы успешно зарегистрированы!")

# Получение курса валют (асинхронный запрос через aiohttp)
@router.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/a1b46b0dd712f7843f62e7a8/latest/USD"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.answer("Не удалось получить данные о курсе валют!")
                return
            data = await response.json()
            usd_to_rub = data['conversion_rates'].get('RUB')
            eur_to_rub = data['conversion_rates'].get('EUR') * usd_to_rub

            if usd_to_rub and eur_to_rub:
                await message.answer(
                    f"💵 1 USD - {usd_to_rub:.2f} RUB\n"
                    f"💶 1 EUR - {eur_to_rub:.2f} RUB"
                )
            else:
                await message.answer("Ошибка при получении данных.")
# Основная функция запуска бота
async def main():
    await setup_db()
    dp.include_router(router)

    print("🚀 Бот запущен! Нажмите Ctrl + C для выхода.")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        print("✅ Сессия бота закрыта.")

# Запуск
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Бот выключен через Ctrl + C.")
