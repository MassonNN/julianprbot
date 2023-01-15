"""
    Структура клавиатуры отмены
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Твои посты'), KeyboardButton(text='Твои каналы'), ],
        [KeyboardButton(text='Аккаунт'),
         KeyboardButton(
             text='WebApp',
             web_app=WebAppInfo(url='https://massonnn.github.io/just-test-pages/')
         )],
    ],
    resize_keyboard=True
)
