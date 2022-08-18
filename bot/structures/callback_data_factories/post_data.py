"""
    Callback data для постов
"""
import enum

from aiogram.dispatcher.filters.callback_data import CallbackData


class PostCDAction(enum.IntEnum):
    """
        Действия с постами
    """
    CREATE = 0
    GET = 1


class PostCD(CallbackData, prefix='post'):
    """
        Обработка получения поста
    """
    action: PostCDAction
    post_id: int = None