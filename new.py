#new.py
import asyncio

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN, WEATHER_API_KEY

import aiohttp
import logging
import sqlite3

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS students  (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  name TEXT NOT NULL,
	  age INTEGER NOT NULL,
	  grade TEXT NOT NULL)
    ''')
 
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какой ты группы?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state:FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
            INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    # async with aiohttp.ClientSession() as session:
    #       async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={WEATHER_API_KEY}&units=metric") as response:
    #           if response.status == 200:
    #               weather_data = await response.json()
    #               main = weather_data['main']
    #               weather = weather_data['weather'][0]

    #               temperature = main['temp']
    #               humidity = main['humidity']
    #               description = weather['description']

    #               weather_report = (f"Город - {user_data['city']}\n"
    #                                 f"Температура - {temperature}\n"
    #                                 f"Влажность воздуха - {humidity}\n"
    #                                 f"Описание погоды - {description}")
    #               await message.answer(weather_report)
    #           else:
    #               await message.answer("Не удалось получить данные о погоде")
    # await state.clear()

async def main():
     # Регистрация всех маршрутов
    dp.include_router(router)

    print("🚀 Бот запущен! Нажмите Ctrl + C для выхода.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        print("✅ Сессия бота закрыта.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Бот выключен через Ctrl + C.")