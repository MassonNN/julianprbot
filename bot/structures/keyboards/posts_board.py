"""
    Клавиатура для отображения постов
"""
from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.post import Post
from bot.structures.callback_data_factories import PostCD, PostCDAction

POSTS_EDIT_BOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Посмотреть статистику', callback_data=PostCD(action=PostCDAction.STATS).pack()),
            InlineKeyboardButton(text='Рекламировать', callback_data=PostCD(action=PostCDAction.PR).pack()),
        ], [
            InlineKeyboardButton(text='Удалить', callback_data=PostCD(action=PostCDAction.DELETE).pack()),
            InlineKeyboardButton(text='Назад', callback_data='menu'),
        ],
    ]
)


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
