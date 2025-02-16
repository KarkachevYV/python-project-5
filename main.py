#main.py
import asyncio
import aiohttp
from gtts import gTTS
import os
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import API_TOKEN, WEATHER_API_KEY
import random
from googletrans import Translator 


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()

translator = Translator()  # Создаем экземпляр переводчика

async def main():
     # Регистрация всех маршрутов
    dp.include_router(router)

    print("🚀 Бот запущен! Нажмите Ctrl + C для выхода.")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        print("✅ Сессия бота закрыта.")


@router.message(Command(commands=['help']))
async def help_cmd(message: Message):
    """Вывод списка команд"""
    help_text = (
        "🛠 Доступные команды:\n\n"
        "📌 /start — Запустить бота.\n"
        "📌 /help — Показать это сообщение.\n"
        "📌 /weather🌍 Узнать погоду в городе\n" 
        "📌  Хотите узнать об ИИ наберите - что такое ИИ?\n"
        "📌 /photo — рандомное (случайное) фото.\n" 
        "📌 /audio — Загрузить аудио.\n"
        "📌 /video — Загрузить видео.\n"
        "📌 /training — Загрузить видео.\n"
    )
    await message.answer(help_text)

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Hi, {message.from_user.full_name}')


# Определяем состояние
class WeatherState(StatesGroup):
    waiting_for_city = State()

async def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                weather = data['weather'][0]['description']
                temp = data['main']['temp']
                return f"Погода в {city}: {weather}, температура: {temp}°C"
            else:
                return "Не удалось получить данные о погоде. Проверьте название города."

@router.message(Command("weather"))
async def weather_cmd(message: Message, state: FSMContext):
    """Запрос города у пользователя"""
    await message.answer("🌍 Введите название города, чтобы получить погоду. Чтобы отключить режим наберите /cancel")
    await state.set_state(WeatherState.waiting_for_city)

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    """Выход из режима """    
    await state.clear()
    await message.answer("🚫 Режим  отключен.")

@router.message(WeatherState.waiting_for_city)
async def city_handler(message: Message, state: FSMContext):
    """Обрабатывает введённый пользователем город"""
    city = message.text.strip()
    weather_info = await get_weather(city)
    await message.answer(weather_info)

@router.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект (ИИ) — это способность компьютеров или машин выполнять задачи, которые обычно требуют человеческого ума.')


@router.message(F.photo)
async def react_photo(message: Message):
      list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
      rand_answ = random.choice(list)
      await message.answer(rand_answ)
      await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@router.message(Command('photo', prefix='&'))
async def photo(message: Message):
      list = ['https://ru.wikihow.com/узнать-адрес-(URL)-изображения#/Файл:Get-the-URL-for-Pictures-Step-5-Version-3.jpg', 'https://www.wikihow.com/images/thumb/2/21/Get-the-URL-for-Pictures-Step-5-Version-3.jpg/v4-728px-Get-the-URL-for-Pictures-Step-5-Version-3.jpg']
      rand_photo = random.choice(list)
      await message.answer_photo(rand_photo, 'Это очень крутое фото')

@router.message(Command('video'))
async def video(message: Message):
    video = FSInputFile("WhatsApp.mp4")
    await bot.send_chat_action(message.chat.id, 'upload_video')
    await bot.send_video(message.chat.id, video)


@router.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile("signal-vyizova-2.mp3")
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    await bot.send_audio(message.chat.id, audio)


@router.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

  #  tts = gTTS(text=rand_tr, lang='ru')
  #  tts.save("training.mp3")
  
  #  audio = FSInputFile('training.mp3')
  #  await bot.send_audio(message.chat.id, audio)
  #  os.remove("training.mp3")
   tts = gTTS(text=rand_tr, lang='ru')
   tts.save("training.ogg")
   audio = FSInputFile("training.ogg")
   await bot.send_voice(chat_id=message.chat.id, voice=audio)
   os.remove("training.ogg")


@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("sample1.ogg")
    await message.answer_voice(voice)


@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("karkach_bot.pdf")
    await bot.send_document(message.chat.id, doc)


@router.message(F.text)
async def translate_text(message: Message):
    """Перевод текста на английский"""
    translated = translator.translate(message.text, dest='en')
    await message.answer(f"Перевод: {translated.text}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Бот выключен через Ctrl + C.")