#  Copyright (c) 2022.

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import any_state
from aiogram.types import ContentType
from aiogram.utils.i18n import lazy_gettext as __

from bot.handlers.create_post import menu_posts_create, menu_posts_create_text, menu_posts_create_url, \
    menu_posts_create_prtype, menu_posts_create_prtype_url, menu_posts_create_prtype_pub, menu_posts_create_subs_min
from bot.handlers.get_post import menu_posts_get
from bot.handlers.help import help_command, help_func, call_help_func
from bot.handlers.start import (
    start,
    menu_posts,
    menu_account,
    menu_channels,
    PostStates, call_start
)
from bot.structures.callback_data_factories import PostCD, PostCDAction

__all__ = ('register_user_commands', 'bot_commands', 'register_user_handlers',)


def register_user_commands(router: Router) -> None:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(start, CommandStart())
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(start, F.text == __('Старт'))
    router.message.register(menu_posts, F.text == __('Твои посты'))
    router.message.register(menu_account, F.text == __('Аккаунт'), F.content_type == [ContentType.CONTACT, ])
    router.message.register(menu_channels, F.text == __('Твои каналы'))
    router.message.register(menu_posts_create_text, PostStates.waiting_for_text)
    router.message.register(menu_posts_create_subs_min, PostStates.waiting_for_post_subs_min)
    router.message.register(menu_posts_create_prtype_url, PostStates.waiting_for_price_url)
    router.message.register(menu_posts_create_prtype_pub, PostStates.waiting_for_price_publication)
    router.message.register(menu_posts_create_prtype, PostStates.waiting_for_pr_type)
    router.message.register(menu_posts_create_url,
                            PostStates.waiting_for_url)
    router.message.register(help_func, F.text == __('Помощь'))

    router.callback_query.register(call_help_func, F.data == 'help', any_state)
    router.callback_query.register(call_start, F.data == 'menu', any_state)
    router.callback_query.register(menu_posts_create,
                                   PostCD.filter(F.action == PostCDAction.CREATE), PostStates.waiting_for_select)
    router.callback_query.register(menu_posts_get,
                                   PostCD.filter(F.action == PostCDAction.GET), PostStates.waiting_for_select)


# Alias
register_user_handlers = register_user_commands
