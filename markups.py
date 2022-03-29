from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup

keyboardStart = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttonsStart = ["Найти фильм", "Случайный фильм", "Инструкция"]
keyboardStart.add(*buttonsStart)

urlbtnChannel1 = InlineKeyboardMarkup(text="Лучшие фильмы", url="https://t.me/watchin_movies")
btnDoneSub = InlineKeyboardMarkup(text="Подписался", callback_data="subDone")

checkSubMenu = InlineKeyboardMarkup(row_width=1)
checkSubMenu.insert(urlbtnChannel1)
checkSubMenu.insert(btnDoneSub)
