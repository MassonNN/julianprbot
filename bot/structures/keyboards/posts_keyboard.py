"""
    Клавиатура для отображения постов
"""
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.post import Post
from bot.structures.callback_data_factories import PostCallbackData

CREATE_NEW_POST = InlineKeyboardButton(text='Создать пост', callback_data='createpost')


def generate_posts_board(posts: List[Post]) -> InlineKeyboardMarkup:
    """
    Сгенерировать клавиатуру с постами
    :param posts: список постов для отображения
    :return:
    """

    builder = InlineKeyboardBuilder()
    for post in posts:
        builder.button(text=post.text[:20], callback_data=PostCallbackData(post_id=post.id))
    builder.add(CREATE_NEW_POST)
    builder.adjust(1)

    return builder.as_markup()

