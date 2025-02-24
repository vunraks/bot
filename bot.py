import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api import TOKEN
import random
import requests
from aiogram import F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ContentType
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Найти информацию", callback_data="find_info")],
            [InlineKeyboardButton(text="Связаться", callback_data="contact")],
            [InlineKeyboardButton(text="О баге", callback_data="about")],
            [InlineKeyboardButton(text="Погода", callback_data="weather")],
            [InlineKeyboardButton(text="Фильмы", callback_data="films")]
            [InlineKeyboardButton(text="Случайное число", callback_data="random")]  
        ]
    )
    return keyboard

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Это тестовый бот",
        reply_markup=get_keyboard()
    )

@dp.message(Command("help"))
async def help_command(message: types.Message):
    command_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показывает список команд\n"
        "/random - Случайное число\n"
        "/weather - Узнать погоду\n"
        "/films - Выбрать фильм"
        "/random - Случайное число"
    )
    await message.answer(command_text)

@dp.message(Command("random"))
async def random_command(message: types.Message):
    number = random.randint(1, 100)
    await message.answer(f"Случайное число: {number}")

@dp.callback_query()
async def callback_handler(callback: types.CallbackQuery):
    if callback.data == "find_info":
        await callback.message.answer("Введите информацию для поиска")
    elif callback.data == "contact":
        await callback.message.answer("Напишите нам в личные сообщения->")
    elif callback.data == "about":
        await callback.message.answer("Это наш бот")
    elif callback.data == "weather":
        await callback.message.answer("Введите название города для получения погоды")
    elif callback.data == "films":
        await cmd_films(callback.message)
    await callback.answer()

@dp.message(Command("weather"))
async def start_weather_command(message: types.Message):
    await message.answer("Введите название города для получения погоды")

btn_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Хоррор"), KeyboardButton(text="Приключения")],
        [KeyboardButton(text="Комедии"), KeyboardButton(text="Фантастика")],
        [KeyboardButton(text="Триллеры")]
    ],
    resize_keyboard=True
)

horror = ["https://www.kinopoisk.ru/film/977288/","https://www.kinopoisk.ru/series/915196/","https://www.kinopoisk.ru/film/195524/"]
adventure = ["https://www.kinopoisk.ru/film/5078983/","https://www.kinopoisk.ru/film/522941/","https://www.kinopoisk.ru/film/427076/"]
comedy = ["https://www.kinopoisk.ru/film/8124/","https://www.kinopoisk.ru/film/42664/","https://www.kinopoisk.ru/film/6039/"]
fantastic = ["https://www.kinopoisk.ru/film/251733/","https://www.kinopoisk.ru/film/258687/","https://www.kinopoisk.ru/film/447301/"]
triller = ["https://www.kinopoisk.ru/film/397667/","https://www.kinopoisk.ru/film/361/","https://www.kinopoisk.ru/series/838050/"]

genre_dict = {
    "Хоррор": horror,
    "Приключения": adventure,
    "Комедии": comedy,
    "Фантастика": fantastic,
    "Триллеры": triller
}

@dp.message(Command("films"))
async def cmd_films(message: Message):
    await message.answer("Выберите жанр", reply_markup=btn_keyboard)

@dp.message(F.text)
async def handle_text_message(message: Message):
    genre = message.text.strip()
    if genre in genre_dict:
        logging.info(f"Выбран жанр: {genre}")
        film_link = random.choice(genre_dict[genre])
        await message.reply(f"Вот фильм в жанре {genre}: {film_link}")
    else:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347"
            weather_data = requests.get(url).json()
            temperature = weather_data["main"]["temp"]
            temperature_feels = weather_data["main"]["feels_like"]
            wind_speed = weather_data["wind"]["speed"]
            cloud_cover = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]

            await message.answer(f"Температура воздуха: {temperature}°C\n"
                                 f"Ощущается как: {temperature_feels}°C\n"
                                 f"Ветер: {wind_speed} м/с\n"
                                 f"Облачность: {cloud_cover}\n"
                                 f"Влажность: {humidity}%")
        except KeyError:
            await message.answer("Не удалось найти погоду для указанного города. Проверьте название и попробуйте снова.")

# Запуск бота  
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())