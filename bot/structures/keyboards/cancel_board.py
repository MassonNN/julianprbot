"""
    Структура клавиатуры отмены
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


CANCEL_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отмена'), ],
    ],
    resize_keyboard=True
)
