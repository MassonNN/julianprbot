"""
    Структура клавиатуры отмены
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Твои посты'), KeyboardButton(text='Твои каналы'), ],
        [KeyboardButton(text='Аккаунт'), ],
    ],
    resize_keyboard=True
)
