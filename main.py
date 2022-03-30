import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from settings import CONFIG_TOKEN, HOST_NAME
import httpx
import logging
import markups

bot = Bot(token=CONFIG_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
channel_id_1 = "@watchin_movies"
# logging.basicConfig(level=logging.INFO) - в текущей ситуации - мусор, продумать логирование в бд


@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    if sub_chanels_check(await bot.get_chat_member(chat_id=channel_id_1, user_id=message.from_user.id)):
        await message.answer("Привет! Нажми нужную кнопку", reply_markup=markups.keyboardStart)
    else:
        await message.answer("Для того, чтобы использовать бот, нужно подписаться на канал!", reply_markup=markups.checkSubMenu)


@dp.callback_query_handler(text="subDone")
async def subChanelDone(message: types.Message):
    # await bot.delete_message(message.from_user.id, message.message.message_id)
    if sub_chanels_check(await bot.get_chat_member(chat_id=channel_id_1, user_id=message.from_user.id)):
        await message.answer("Привет! Нажми нужную кнопку", reply_markup=markups.keyboardStart)
    else:
        await message.answer("Для того, чтобы использовать бот, нужно подписаться на канал!", reply_markup=markups.checkSubMenu)


@dp.message_handler(lambda message: message.text == "Инструкция")
async def cmd_test1(message: types.Message):
    await message.answer("Привет! Я - умный бот, предназначенный для поиска фильма на вечер! \n Найти фильм - "
                         "дописать. \nСлучайный фильм - дописать")


@dp.message_handler(lambda message: message.text == "Найти фильм")
async def cmd_film(message: types.Message):
    await message.answer("Введите номер фильма")
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
        await message.answer("Что-то пошло не так... Попробуйте еще раз")


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
    film_info_ok = 'Название фильма:' + film_name + '\n\n' + 'Описание фильма:' + film_desc + '\n\n' + 'Ссылка на фильм в хорошем качестве:' + film_link
    return film_info_ok


def sub_chanels_check(chat_member):
    print(chat_member['status'])
    if chat_member['status'] != 'left':
        return True
    else:
        return False


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
