"""
    Структура клавиатуры отмены
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


PRTYPE_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Оплата за одну публикацию'),
            KeyboardButton(text='Оплата за переход по ссылке'),
            KeyboardButton(text='Отмена'),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
