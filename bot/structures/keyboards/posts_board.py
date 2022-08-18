"""
    Клавиатура для отображения постов
"""
from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.post import Post
from bot.structures.callback_data_factories import PostCD, PostCDAction


def generate_posts_board(posts: List[Post]) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с постами
    :param posts: список постов для отображения
    :return:
    """

    builder = InlineKeyboardBuilder()
    for post in posts:
        builder.button(text=post.text[:20], callback_data=PostCD(action=PostCDAction.GET, post_id=post.id).pack())
    builder.button(text='Создать пост', callback_data=PostCD(action=PostCDAction.CREATE).pack())
    builder.adjust(1)

    return builder.as_markup()
