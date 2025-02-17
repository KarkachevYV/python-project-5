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
    city = State()

def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users  (
	  id INTEGER PRIMARY KEY AUTOINCREMENT,
	  name TEXT NOT NULL,
	  age INTEGER NOT NULL,
	  city TEXT NOT NULL)
    ''')
 
    conn.commit()
    conn.close()

init_db()

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