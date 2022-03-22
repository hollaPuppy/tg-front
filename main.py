import random
import emoji
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from settings import CONFIG_TOKEN, HOST_NAME
import httpx
import logging


bot = Bot(token=CONFIG_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Найти фильм", "Инструкция", "Случайный фильм"]
    keyboard.add(*buttons)
    await message.answer("Привет! Нажми нужную кнопку", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Инструкция")
async def cmd_test1(message: types.Message):
    await message.answer("Привет! Я - умный бот, предназначенный для поиска фильма на вечер! \nНайти фильм - "
                         "дописать. \nСлучайный фильм - дописать")


@dp.message_handler(lambda message: message.text == "Найти фильм")
async def cmd_film(message: types.Message):
    await message.answer("Вводи номер фильма дура")
    await Mydialog.otvet.set()


@dp.message_handler(lambda message: message.text == "Случайный фильм")
async def cmd_film(message: types.Message):
    await message.answer("Сейчас посмотрим, что же вам посоветовать...")
    try:
        async with httpx.AsyncClient() as client:
            rand_film = random.randint(1, 10)
            film_info_answer = await client.get(f'{HOST_NAME}/get_film_info/{rand_film}')
            film_info = film_info_answer.json()
            film_info_ok = parse_answer_film_info(film_info)
            await message.answer(film_info_ok)
    except BaseException:
        await message.answer("вышел из ренжа лол")


class Mydialog(StatesGroup):
    otvet = State()


@dp.message_handler(state=Mydialog.otvet)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        try:
            async with httpx.AsyncClient() as client:
                film_info_answer = await client.get(f'{HOST_NAME}/get_film_info/{user_message}')
                film_info = film_info_answer.json()
                film_info_ok = parse_answer_film_info(film_info)
                await message.answer(film_info_ok)
        except BaseException:
            await message.answer("Нет фильма с таким номером")
    await state.finish()


def parse_answer_film_info(film_info):
    for each in film_info:
        film_name = f"{each['film_name']}"
        film_desc = f"{each['film_desc']}"
        film_link = f"{each['film_link']}"
    film_info_ok = 'Название фильма:' + film_name + emoji.emojize(
        ' :thumbs_up:') + '\n\n' + 'Описание фильма:' + film_desc + '\n\n' + 'Ссылка на фильм в хорошем качестве:' + film_link
    return film_info_ok


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)