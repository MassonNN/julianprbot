"""
    Callback data для постов
"""
from aiogram.dispatcher.filters.callback_data import CallbackData


class PostCallbackData(CallbackData, prefix='post'):
    """
        Обработка получения поста
    """
    post_id: int
