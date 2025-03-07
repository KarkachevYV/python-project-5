#main.py
import asyncio
import aiohttp
from gtts import gTTS
import os
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN, WEATHER_API_KEY, THE_CAT_API_KEY, NASA_API_KEY, DADATA_API_KEY
import random
from googletrans import Translator 
import keyboards as kb 
import requests
from datetime import datetime, timedelta
from dadata import Dadata

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()
storage = MemoryStorage()

translator = Translator()  # Создаем экземпляр переводчика

# Определяем состояние для перевода
class TranslateState(StatesGroup):
    waiting_for_text = State()


async def main():
     # Регистрация всех маршрутов
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    print("🚀 Бот запущен! Нажмите Ctrl + C для выхода.")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
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
        "📌 /training — Загрузить сообщение.\n"
        "📌 /links — Пример обычных кнопок.\n"
        "📌 /dinamic — Пример динамических инлайн кнопок.\n"
        "📌 /cats — О породах в общих чертах.\n"
        "📌 /random_apod — Сюрприз от NASA.\n"
        "📌 /dadata - Общая информация о стране"
        
    )
    await message.answer(help_text)


@router.callback_query(F.data == "news")
async def news(callback: CallbackQuery):
    await callback.answer('Новости подгружаются', show_alert=True)
    await callback.message.edit_text('Вот свежие новости.', reply_markup=await kb.test_keyboard())

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.main)
    # await message.answer(f'Здравствуй, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)
    # await message.answer(f'Hi, {message.from_user.full_name}', reply_markup=await kb.test_keyboard())

@router.message(F.text == "Привет")
async def test_button(message: Message):
    await message.answer(f'Привет,{message.from_user.full_name}')


@router.message(F.text == "Пока")
async def test_button(message: Message):
    await message.answer(f'Пока,{message.from_user.full_name}')


# @router.message(F.text == "Тестовая кнопка 1")
# async def test_button(message: Message):
#     await message.answer('Обработка на нажатие на Reply кнопку.')

# @router.message(Command("links"))
# async def weather_cmd(message: Message, state: FSMContext):
#     await message.answer(f'Здравствуй, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)

# Обработчик команды /dinamic
@router.message(Command("dinamic"))
async def dynamic_cmd(message: Message):
    await message.answer(f'Hi, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)

# Обработчик нажатия на кнопку "Показать больше"
@router.callback_query(F.data == "further")
async def further(callback: CallbackQuery):
    await callback.message.edit_text('Смотреть дальше:', reply_markup=await kb.test_keyboard())

# Обработчики нажатий на кнопки "Опция 1" и "Опция 2"
@router.callback_query(F.data.in_({"Опция 1", "Опция 2"}))
async def option_selected(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'Вы выбрали {callback.data}')


# def get_cat_breeds():
#    url = "https://api.thecatapi.com/v1/breeds"
#    headers = {"x-api-key": THE_CAT_API_KEY}
#    response = requests.get(url, headers=headers)
#    return response.json()

# def get_cat_image_by_breed(breed_id):
#      url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
#      headers = {"x-api-key": THE_CAT_API_KEY}
#      response = requests.get(url, headers=headers)
#      data = response.json()
#      return data[0]['url']

# def get_breed_info(breed_name):
#    breeds = get_cat_breeds()
#    for breed in breeds:
#         if breed['name'].lower() == breed_name.lower():
#             # Переводим описание породы на русский
#             description_ru = translator.translate(breed['description'], dest='ru').text
#             return {
#                 'name': breed['name'],
#                 'description': description_ru,
#                 'life_span': breed['life_span'],
#                 'id': breed['id']
#             }
#    return None

# @router.message(Command("cats"))
# async def cats(message: Message):
#    await message.answer("Привет! Напиши мне название породы кошки, и я пришлю тебе её фото и описание.")


# @router.message()
# async def send_cat_info(message: Message):
#    translated = translator.translate(message.text, dest='en')
#    breed_name = translated.text
#    breed_info = get_breed_info(breed_name)
#    if breed_info:
#        cat_image_url = get_cat_image_by_breed(breed_info['id'])
#        info = (
#            f"Порода - {breed_info['name']}\\n"
#            f"Описание - {breed_info['description']}\\n"
#            f"Продолжительность жизни - {breed_info['life_span']} лет"
#        )
#        await message.answer_photo(photo=cat_image_url, caption=info)
#    else:
#        await message.answer("Порода не найдена. Попробуйте еще раз.")


def get_random_apod():
   end_date = datetime.now() # конечная дата - сегодня
   start_date = end_date - timedelta(days=365)
   random_date = start_date + (end_date - start_date) * random.random()
   date_str = random_date.strftime("%Y-%m-%d")

   url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
   response = requests.get(url)
   return response.json()

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
   apod = get_random_apod()
   photo_url = apod['url']
  #  title = apod['title']
   title_ru = translator.translate(apod['title'], dest='ru').text

   await message.answer_photo(photo=photo_url, caption=f"{title_ru}")


class TextFilter(BaseFilter):
    def __init__(self, text: str, ignore_case: bool = False):
        self.text = text.lower() if ignore_case else text
        self.ignore_case = ignore_case

    async def __call__(self, message: Message) -> bool:
        message_text = message.text.lower() if self.ignore_case else message.text
        return message_text == self.text

async def fetch_country_info(country_name):
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/country"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {"query": country_name}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result['suggestions']
            else:
                return None

@router.message(Command("dadata"))
async def send_welcome(message: Message):
    await message.reply("Привет! Напиши название страны, и я постараюсь найти информацию о ней.")

@router.message(TextFilter(text='страны', ignore_case=True))
async def list_countries(message: Message):
    await message.reply("Напишите название страны, чтобы получить информацию о ней.")

# @router.message()
# async def get_country_info(message: Message, state: FSMContext):
#     # translated = translator.translate(message.text, dest='en')
#     country_name = message.text
#     suggestions = await fetch_country_info(country_name)
#     if suggestions:
#         response = "\n".join([sug['value'] for sug in suggestions])
#         await message.reply(f"Информация о стране:\n{response}")
#     else:
#         await message.reply("Не удалось найти информацию о данной стране.")
@router.message()
async def get_country_info(message: Message, state: FSMContext):
    country_name = message.text
    suggestions = await fetch_country_info(country_name)
    if suggestions:
        response_lines = []
        for suggestion in suggestions:
            value = suggestion.get('unrestricted_value', 'Неизвестно')
            code = suggestion.get('data', {}).get('code', 'Нет данных')
            iso_code = suggestion.get('data', {}).get('iso_code', 'Нет данных')
            response_lines.append(f"Страна: {value}, Код: {code}, ISO Код: {iso_code}")
        
        response = "\n".join(response_lines)
        await message.reply(f"Информация о стране:\n{response}")
    else:
        await message.reply("Не удалось найти информацию о данной стране.")

#  Определяем состояние
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