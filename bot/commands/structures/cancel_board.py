"""
    Структура клавиатуры отмены
"""
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_board() -> ReplyKeyboardMarkup:
    """
    Получить клавиатуру отмены
    :return:
    """
    rk_builder = ReplyKeyboardBuilder()
    rk_builder.button('Отмена')
    return rk_builder.as_markup(resize_keyboard=True)
